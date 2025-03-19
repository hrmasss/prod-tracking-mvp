from django.contrib import admin
from django.utils.html import format_html
from common.admin import BaseModelAdmin, TabularInline
from tracker.utils import (
    generate_material_qr_code,
    render_qr_code,
    generate_bundle_qr_code,
    render_combined_qr_codes,
)
from tracker.models import (
    Buyer,
    Season,
    Style,
    Material,
    MaterialPiece,
    ProductionLine,
    Scanner,
    ScanEvent,
    ProductionBatch,
    Size,
    Bundle,
    QualityCheck,
    ReworkAssignment,
)


class MaterialInline(TabularInline):
    model = Material
    extra = 0


class MaterialPieceInline(TabularInline):
    model = MaterialPiece
    extra = 0
    readonly_fields = ["qr_image_display"]
    fields = ["qr_image_display"]

    def qr_image_display(self, obj):
        return render_qr_code(obj)

    qr_image_display.short_description = "QR Code"

    def save_model(self, request, obj, form, change):
        # Generate QR code if it doesn't exist
        if not obj.qr_code:
            generate_material_qr_code(obj)
        super().save_model(request, obj, form, change)


class BundleInline(TabularInline):
    model = Bundle
    extra = 0
    readonly_fields = ["qr_image_display"]
    fields = ["production_batch", "material", "size", "quantity", "qr_image_display"]

    def qr_image_display(self, obj):
        return render_qr_code(obj)

    qr_image_display.short_description = "QR Code"

    def save_model(self, request, obj, form, change):
        # Generate QR code if it doesn't exist
        if not obj.qr_code:
            generate_bundle_qr_code(obj)
        super().save_model(request, obj, form, change)


class ScannerInline(TabularInline):
    model = Scanner
    extra = 0


@admin.register(Buyer)
class BuyerAdmin(BaseModelAdmin):
    list_display = ("name", "created_at", "updated_at")


@admin.register(Season)
class SeasonAdmin(BaseModelAdmin):
    list_display = ("name", "created_at", "updated_at")


@admin.register(Size)
class SizeAdmin(BaseModelAdmin):
    list_display = ("name", "created_at", "updated_at")


@admin.register(Style)
class StyleAdmin(BaseModelAdmin):
    list_display = ("buyer", "season", "style_name", "created_at", "updated_at")
    list_filter = ("buyer", "season")
    filter_horizontal = ("sizes",)
    inlines = [MaterialInline]


@admin.register(Material)
class MaterialAdmin(BaseModelAdmin):
    list_display = ("style", "name")
    list_filter = ("style",)


@admin.register(Bundle)
class BundleAdmin(BaseModelAdmin):
    list_display = (
        "production_batch",
        "material",
        "size",
        "quantity",
        "qr_code",
        "qr_image_display",
        "created_at",
        "updated_at",
    )
    list_filter = ("production_batch", "material", "size")
    readonly_fields = ["qr_code", "qr_image_display", "print_pieces_qr_codes"]
    fields = [
        "production_batch",
        "material",
        "size",
        "quantity",
        "qr_image_display",
        "print_pieces_qr_codes",
    ]
    inlines = [MaterialPieceInline]

    def qr_image_display(self, obj):
        return render_qr_code(obj)

    qr_image_display.short_description = "QR Code"

    def print_pieces_qr_codes(self, obj):
        pieces = obj.material_pieces.all()
        return render_combined_qr_codes(pieces)  # Use the new function

    print_pieces_qr_codes.short_description = "Print All Pieces QR Codes"


@admin.register(MaterialPiece)
class MaterialPieceAdmin(BaseModelAdmin):
    list_display = (
        "bundle",
        "qr_code",
        "qr_image_display",
        "current_production_line",
        "created_at",
        "updated_at",
    )
    list_filter = ("bundle", "current_production_line")
    readonly_fields = ["qr_code", "qr_image_display"]
    fields = ["bundle", "qr_code", "qr_image_display", "current_production_line"]

    def qr_image_display(self, obj):
        return render_qr_code(obj)

    qr_image_display.short_description = "QR Code"


@admin.register(ProductionBatch)
class ProductionBatchAdmin(BaseModelAdmin):
    list_display = ("style", "batch_number", "created_at", "updated_at")
    inlines = [BundleInline]
    filter_horizontal = ("production_lines",)


@admin.register(ProductionLine)
class ProductionLineAdmin(BaseModelAdmin):
    list_display = ("name", "location", "created_at", "updated_at")
    inlines = [ScannerInline]


@admin.register(Scanner)
class ScannerAdmin(BaseModelAdmin):
    list_display = ("name", "production_line", "type", "created_at", "updated_at")
    list_filter = ("production_line", "type")


@admin.register(ScanEvent)
class ScanEventAdmin(BaseModelAdmin):
    list_display = ("scanner", "material_piece", "scan_time")
    list_filter = ("scanner", "scan_time")


@admin.register(QualityCheck)
class QualityCheckAdmin(BaseModelAdmin):
    list_display = ("scan_event", "status", "defect_code", "created_at", "updated_at")
    list_filter = ("status", "defect_code")


@admin.register(ReworkAssignment)
class ReworkAssignmentAdmin(BaseModelAdmin):
    list_display = (
        "quality_check",
        "rework_production_line",
        "rework_completed",
        "created_at",
        "updated_at",
    )
    list_filter = ("rework_production_line", "rework_completed")
