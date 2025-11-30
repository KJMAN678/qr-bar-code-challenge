from django.db import models


class CodeType(models.TextChoices):
    """コードの種類（QRコードまたはバーコード）"""

    QR_CODE = "qr_code", "QRコード"
    BARCODE = "barcode", "バーコード"


class QRCodeFormat(models.TextChoices):
    """QRコードの規格"""

    QR_CODE = "qr_code", "QRコード"
    MICRO_QR = "micro_qr", "マイクロQR"


class BarcodeFormat(models.TextChoices):
    """バーコードの規格"""

    CODE39 = "code39", "Code39"
    CODE128 = "code128", "Code128"
    EAN13 = "ean13", "EAN-13"
    EAN8 = "ean8", "EAN-8"
    UPCA = "upca", "UPC-A"
    UPCE = "upce", "UPC-E"
    ITF = "itf", "ITF"


class CodeData(models.Model):
    """QRコード/バーコードのデータを保存するモデル"""

    text = models.TextField(verbose_name="テキスト", help_text="QRコード/バーコードにしたいテキスト")
    code_type = models.CharField(
        max_length=20,
        choices=CodeType.choices,
        default=CodeType.QR_CODE,
        verbose_name="コードの種類",
        help_text="QRコードまたはバーコードを選択",
    )
    qr_format = models.CharField(
        max_length=20,
        choices=QRCodeFormat.choices,
        default=QRCodeFormat.QR_CODE,
        blank=True,
        verbose_name="QRコード規格",
        help_text="QRコードの場合の規格",
    )
    barcode_format = models.CharField(
        max_length=20,
        choices=BarcodeFormat.choices,
        default=BarcodeFormat.CODE128,
        blank=True,
        verbose_name="バーコード規格",
        help_text="バーコードの場合の規格",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "コードデータ"
        verbose_name_plural = "コードデータ"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.get_code_type_display()}: {self.text[:50]}"
