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


class Size(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Color(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Style(BaseModel):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name="styles")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="styles")
    style_name = models.CharField(max_length=100)
    buyer_contract_number = models.CharField(max_length=200, blank=True, null=True)
    sizes = models.ManyToManyField(Size, related_name="styles", blank=True)
    colors = models.ManyToManyField(Color, related_name="styles", blank=True)

    def __str__(self):
        return f"{self.buyer} - {self.season} - {self.style_name}"

    class Meta:
        unique_together = ("buyer", "season", "style_name")


class MaterialType(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Material(BaseModel):
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name="materials")
    name = models.CharField(max_length=100)
    material_type = models.ForeignKey(
        MaterialType, on_delete=models.CASCADE, related_name="materials"
    )
    unit = models.CharField(max_length=20, default="pcs")
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, related_name="materials", null=True, blank=True
    )

    def __str__(self):
        return f"{self.style} - {self.name} ({self.material_type})"


class Operation(BaseModel):
    class OperationCategory(models.TextChoices):
        CUTTING = "CUTTING", "Cutting"
        SEWING = "SEWING", "Sewing"
        FINISHING = "FINISHING", "Finishing"
        PACKING = "PACKING", "Packing"
        QUILTING = "QUILTING", "Quilting"
        DOWNFILLING = "DOWNFILLING", "Downfilling"

    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(
        max_length=20,
        choices=OperationCategory.choices,
        default=OperationCategory.SEWING,
    )
    sequence = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["sequence"]


class ProductionLine(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    operation_type = models.CharField(
        max_length=20,
        choices=Operation.OperationCategory.choices,
        default=Operation.OperationCategory.SEWING,
    )
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


class Bundle(BaseModel):
    production_batch = models.ForeignKey(
        ProductionBatch, on_delete=models.CASCADE, related_name="bundles"
    )
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name="bundles"
    )
    size = models.ForeignKey(
        Size, on_delete=models.CASCADE, related_name="bundles", null=True, blank=True
    )
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, related_name="bundles", null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=1)
    qr_code = models.CharField(max_length=255, unique=True, blank=True, null=True)
    qr_image = OptimizedImageField(
        upload_to="bundle_qr_codes/", blank=True, null=True, max_dimensions=(400, 400)
    )

    def __str__(self):
        return f"Bundle for {self.material} ({self.size}) ({self.color}) - Batch {self.production_batch.batch_number}"


class MaterialPiece(BaseModel):
    bundle = models.ForeignKey(
        Bundle, on_delete=models.CASCADE, related_name="material_pieces"
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

    def __str__(self):
        return f"{self.bundle} - Piece {self.id}"


class Scanner(BaseModel):
    class ScannerType(models.TextChoices):
        IN = "IN", "In"
        OUT = "OUT", "Out"
        QC = "QC", "Quality Control"

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


class Defect(BaseModel):
    type = models.CharField(
        max_length=20,
        choices=Operation.OperationCategory.choices,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    severity_level = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        unique_together = ("type", "name")


class QualityCheck(BaseModel):
    class QualityStatus(models.TextChoices):
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"
        REWORK = "REWORK", "Rework"

    scan_event = models.OneToOneField(
        "ScanEvent", on_delete=models.CASCADE, related_name="quality_check"
    )
    status = models.CharField(
        max_length=10, choices=QualityStatus.choices, default=QualityStatus.ACCEPTED
    )
    defects = models.ManyToManyField(Defect, related_name="quality_checks", blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"QC - {self.scan_event.material_piece} - {self.status}"


class ReworkAssignment(BaseModel):
    quality_check = models.OneToOneField(
        QualityCheck, on_delete=models.CASCADE, related_name="rework_assignment"
    )
    rework_production_line = models.ForeignKey(
        ProductionLine,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rework_assignments",
    )
    rework_notes = models.TextField(blank=True, null=True)
    rework_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Rework - {self.quality_check.scan_event.material_piece}"


class ScanEvent(BaseModel):
    scanner = models.ForeignKey(
        Scanner, on_delete=models.CASCADE, related_name="scan_events"
    )
    material_piece = models.ForeignKey(
        MaterialPiece,
        on_delete=models.CASCADE,
        related_name="scan_events",
    )
    scan_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scan Event - {self.scan_time}"


class ProductionTarget(BaseModel):
    production_line = models.ForeignKey(
        ProductionLine, on_delete=models.CASCADE, related_name="targets"
    )
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name="targets")
    date = models.DateField()
    target_quantity = models.PositiveIntegerField()
    actual_quantity = models.PositiveIntegerField(default=0)

    def efficiency_percentage(self):
        if self.target_quantity > 0:
            return (self.actual_quantity / self.target_quantity) * 100
        return 0

    class Meta:
        unique_together = ("production_line", "style", "date")
