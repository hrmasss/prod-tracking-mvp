from django.db import models
from common.models import BaseModel
from common.fields import OptimizedImageField
from tracker.utils import material_qr_image_upload_path, bundle_qr_image_upload_path


class Buyer(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Season(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Style(BaseModel):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name="styles")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="styles")
    style_number = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.buyer} - {self.season} - {self.style_number}"

    class Meta:
        unique_together = ("buyer", "season", "style_number")


class MaterialPiece(BaseModel):
    style = models.ForeignKey(
        Style, on_delete=models.CASCADE, related_name="material_pieces"
    )
    name = models.CharField(max_length=100)
    qr_code = models.CharField(max_length=255, unique=True, blank=True, null=True)
    qr_image = OptimizedImageField(
        upload_to=material_qr_image_upload_path,
        blank=True,
        null=True,
        max_dimensions=(400, 400),
    )

    def __str__(self):
        return f"{self.style} - {self.name}"


class Bundle(BaseModel):
    name = models.CharField(max_length=100)
    pieces = models.ManyToManyField(MaterialPiece, related_name="bundles", blank=True)
    qr_code = models.CharField(max_length=255, unique=True, blank=True, null=True)
    qr_image = OptimizedImageField(
        upload_to=bundle_qr_image_upload_path,
        blank=True,
        null=True,
        max_dimensions=(400, 400),
    )

    def __str__(self):
        return self.name


class ProductionLine(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Scanner(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    production_line = models.ForeignKey(
        ProductionLine,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="scanners",
    )

    def __str__(self):
        return self.name


class ScanEvent(BaseModel):
    scanner = models.ForeignKey(
        Scanner, on_delete=models.CASCADE, related_name="scan_events"
    )
    material_piece = models.ForeignKey(
        MaterialPiece,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="scan_events",
    )
    bundle = models.ForeignKey(
        Bundle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="scan_events",
    )
    scan_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scan Event - {self.scan_time}"
