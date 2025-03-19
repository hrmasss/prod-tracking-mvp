from django.db import models
from common.models import BaseModel
from common.fields import OptimizedImageField
from tracker.utils import material_qr_image_upload_path


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


class Material(BaseModel):
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name="materials")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.style} - {self.name}"


class MaterialPiece(BaseModel):
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name="material_pieces"
    )
    qr_code = models.CharField(max_length=255, unique=True, blank=True, null=True)
    qr_image = OptimizedImageField(
        upload_to=material_qr_image_upload_path,
        blank=True,
        null=True,
        max_dimensions=(400, 400),
    )
    current_production_line = models.ForeignKey(
        "ProductionLine",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="current_material_pieces",
    )
    production_flow = models.ManyToManyField(
        "ProductionLine", related_name="material_flow", blank=True
    )
    production_batch = models.ForeignKey(
        "ProductionBatch",
        on_delete=models.CASCADE,
        related_name="material_pieces",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.material.style} - {self.material.name} - {self.id}"


class ProductionLine(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class ProductionBatch(BaseModel):
    style = models.ForeignKey(
        Style, on_delete=models.CASCADE, related_name="production_batches"
    )
    production_lines = models.ManyToManyField(
        ProductionLine, related_name="production_batches", blank=True
    )
    batch_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.style} - Batch {self.batch_number}"


class Scanner(BaseModel):
    class ScannerType(models.TextChoices):
        IN = "IN", "In"
        OUT = "OUT", "Out"

    name = models.CharField(max_length=100, unique=True)
    production_line = models.ForeignKey(
        ProductionLine,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="scanners",
    )
    type = models.CharField(
        max_length=4, choices=ScannerType.choices, default=ScannerType.IN
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
    scan_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scan Event - {self.scan_time}"
