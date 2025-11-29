from datetime import datetime
from typing import Literal

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema

from api.models import BarcodeFormat, CodeData, CodeType, QRCodeFormat

api = NinjaAPI()


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
    code = CodeData.objects.create(**payload.dict())
    return code


@api.put("/codes/{code_id}", response=CodeDataSchema)
def update_code(request: HttpRequest, code_id: int, payload: CodeDataUpdateSchema) -> CodeData:
    code = get_object_or_404(CodeData, id=code_id)
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
