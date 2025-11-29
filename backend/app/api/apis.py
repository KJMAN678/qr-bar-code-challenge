import re
from datetime import datetime
from typing import Literal

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema
from ninja.errors import HttpError

from api.models import BarcodeFormat, CodeData, CodeType, QRCodeFormat

api = NinjaAPI()


def validate_barcode_text(text: str, barcode_format: str) -> None:
    """バーコード規格に応じたテキストのバリデーション"""
    if barcode_format == "code39":
        if not re.match(r"^[A-Z0-9\-. $/+%]*$", text.upper()):
            raise HttpError(
                400,
                "Code39は英大文字、数字、および記号(- . $ / + % スペース)のみ対応しています",
            )
    elif barcode_format == "code128":
        try:
            text.encode("ascii")
        except UnicodeEncodeError:
            raise HttpError(400, "Code128はASCII文字のみ対応しています（日本語不可）")
    elif barcode_format == "ean13":
        if not re.match(r"^\d{12,13}$", text):
            raise HttpError(400, "EAN-13は12桁または13桁の数字のみ対応しています")
    elif barcode_format == "ean8":
        if not re.match(r"^\d{7,8}$", text):
            raise HttpError(400, "EAN-8は7桁または8桁の数字のみ対応しています")
    elif barcode_format == "upca":
        if not re.match(r"^\d{11,12}$", text):
            raise HttpError(400, "UPC-Aは11桁または12桁の数字のみ対応しています")
    elif barcode_format == "upce":
        if not re.match(r"^\d{6,8}$", text):
            raise HttpError(400, "UPC-Eは6桁から8桁の数字のみ対応しています")
    elif barcode_format == "itf":
        if not re.match(r"^\d+$", text) or len(text) % 2 != 0:
            raise HttpError(400, "ITFは偶数桁の数字のみ対応しています")


def validate_code_type_format(
    code_type: str, qr_format: str | None, barcode_format: str | None
) -> None:
    """コード種類と規格の整合性をバリデーション"""
    if code_type == "qr_code":
        if barcode_format and barcode_format not in ["code128", ""]:
            pass
        qr_valid_formats = [choice[0] for choice in QRCodeFormat.choices]
        if qr_format and qr_format not in qr_valid_formats:
            raise HttpError(
                400,
                f"QRコードの規格は {', '.join(qr_valid_formats)} のみ選択可能です",
            )
    elif code_type == "barcode":
        barcode_valid_formats = [choice[0] for choice in BarcodeFormat.choices]
        if barcode_format and barcode_format not in barcode_valid_formats:
            raise HttpError(
                400,
                f"バーコードの規格は {', '.join(barcode_valid_formats)} のみ選択可能です",
            )
        qr_valid_formats = [choice[0] for choice in QRCodeFormat.choices]
        if qr_format and qr_format not in qr_valid_formats:
            pass


class CodeDataSchema(Schema):
    id: int
    text: str
    code_type: str
    qr_format: str
    barcode_format: str
    created_at: datetime
    updated_at: datetime


class CodeDataCreateSchema(Schema):
    text: str
    code_type: Literal["qr_code", "barcode"] = "qr_code"
    qr_format: Literal["qr_code", "micro_qr"] = "qr_code"
    barcode_format: Literal["code39", "code128", "ean13", "ean8", "upca", "upce", "itf"] = "code128"


class CodeDataUpdateSchema(Schema):
    text: str | None = None
    code_type: Literal["qr_code", "barcode"] | None = None
    qr_format: Literal["qr_code", "micro_qr"] | None = None
    barcode_format: Literal["code39", "code128", "ean13", "ean8", "upca", "upce", "itf"] | None = None


class CodeTypeChoicesSchema(Schema):
    code_types: list[dict[str, str]]
    qr_formats: list[dict[str, str]]
    barcode_formats: list[dict[str, str]]


@api.get("/")
def index(request: HttpRequest) -> dict[str, int]:
    return {"test": 1}


@api.get("/codes", response=list[CodeDataSchema])
def list_codes(request: HttpRequest) -> list[CodeData]:
    return list(CodeData.objects.all())


@api.get("/codes/{code_id}", response=CodeDataSchema)
def get_code(request: HttpRequest, code_id: int) -> CodeData:
    return get_object_or_404(CodeData, id=code_id)


@api.post("/codes", response=CodeDataSchema)
def create_code(request: HttpRequest, payload: CodeDataCreateSchema) -> CodeData:
    validate_code_type_format(payload.code_type, payload.qr_format, payload.barcode_format)
    if payload.code_type == "barcode":
        validate_barcode_text(payload.text, payload.barcode_format)
    code = CodeData.objects.create(**payload.dict())
    return code


@api.put("/codes/{code_id}", response=CodeDataSchema)
def update_code(request: HttpRequest, code_id: int, payload: CodeDataUpdateSchema) -> CodeData:
    code = get_object_or_404(CodeData, id=code_id)
    
    new_code_type = payload.code_type if payload.code_type is not None else code.code_type
    new_qr_format = payload.qr_format if payload.qr_format is not None else code.qr_format
    new_barcode_format = payload.barcode_format if payload.barcode_format is not None else code.barcode_format
    new_text = payload.text if payload.text is not None else code.text
    
    validate_code_type_format(new_code_type, new_qr_format, new_barcode_format)
    if new_code_type == "barcode":
        validate_barcode_text(new_text, new_barcode_format)
    
    for attr, value in payload.dict(exclude_unset=True).items():
        if value is not None:
            setattr(code, attr, value)
    code.save()
    return code


@api.delete("/codes/{code_id}")
def delete_code(request: HttpRequest, code_id: int) -> dict[str, bool]:
    code = get_object_or_404(CodeData, id=code_id)
    code.delete()
    return {"success": True}


@api.get("/choices", response=CodeTypeChoicesSchema)
def get_choices(request: HttpRequest) -> dict[str, list[dict[str, str]]]:
    return {
        "code_types": [{"value": choice[0], "label": choice[1]} for choice in CodeType.choices],
        "qr_formats": [{"value": choice[0], "label": choice[1]} for choice in QRCodeFormat.choices],
        "barcode_formats": [{"value": choice[0], "label": choice[1]} for choice in BarcodeFormat.choices],
    }
