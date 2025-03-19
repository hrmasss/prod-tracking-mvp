from django.contrib import admin
from django.utils.html import format_html
from common.admin import BaseModelAdmin, TabularInline
from tracker.utils import (
    render_qr_code,
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
    Operation,
    Defect,
    Color,
    MaterialType,
    ProductionTarget,
    Order,
    OrderItem,
)


# --- INLINE ADMIN CLASSES ---


class MaterialInline(TabularInline):
    model = Material
    fields = ("name", "material_type", "unit", "color")
    extra = 0


class OrderInline(TabularInline):
    model = Order
    extra = 0
    fields = ("buyer", "season", "style", "order_number", "delivery_date")


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    fields = ("size", "color", "quantity")


class MaterialPieceInline(TabularInline):
    model = MaterialPiece
    extra = 0
    readonly_fields = ["qr_image_display"]
    fields = ["qr_image_display"]

    def qr_image_display(self, obj):
        return render_qr_code(obj)

    qr_image_display.short_description = "QR Code"


class BundleInline(TabularInline):
    model = Bundle
    extra = 0
    readonly_fields = ["qr_image_display"]
    fields = ["production_batch", "material", "size", "quantity", "qr_image_display"]

    def qr_image_display(self, obj):
        return render_qr_code(obj)

    qr_image_display.short_description = "QR Code"


class ScannerInline(TabularInline):
    model = Scanner
    extra = 0
    fields = ("name", "type")


class ScanEventInline(TabularInline):
    model = ScanEvent
    extra = 0
    fields = ("scanner", "material_piece", "scan_time")
    readonly_fields = ("scan_time",)


class DefectInline(TabularInline):
    model = Defect
    extra = 0
    fields = ("name", "type", "severity_level")


class QualityCheckInline(TabularInline):
    model = QualityCheck
    extra = 0
    fields = ("status", "notes")
    filter_horizontal = ("defects",)


class ReworkAssignmentInline(TabularInline):
    model = ReworkAssignment
    extra = 0
    fields = ("rework_production_line", "rework_notes", "rework_completed")


@admin.register(Buyer)
class BuyerAdmin(BaseModelAdmin):
    list_display = ("name", "created_at", "updated_at")


@admin.register(Season)
class SeasonAdmin(BaseModelAdmin):
    list_display = ("name", "created_at", "updated_at")


@admin.register(Size)
class SizeAdmin(BaseModelAdmin):
    list_display = ("name", "created_at", "updated_at")


@admin.register(Color)
class ColorAdmin(BaseModelAdmin):
    list_display = ("name", "created_at", "updated_at")


@admin.register(MaterialType)
class MaterialTypeAdmin(BaseModelAdmin):
    list_display = ("name", "created_at", "updated_at")


@admin.register(Operation)
class OperationAdmin(BaseModelAdmin):
    list_display = ("name", "type", "sequence", "created_at", "updated_at")
    list_filter = ("type",)
    ordering = ["sequence"]


@admin.register(Defect)
class DefectAdmin(BaseModelAdmin):
    list_display = ("name", "type", "severity_level", "created_at", "updated_at")
    list_filter = ("type", "severity_level")


@admin.register(ProductionTarget)
class ProductionTargetAdmin(BaseModelAdmin):
    list_display = (
        "production_line",
        "style",
        "date",
        "target_quantity",
        "actual_quantity",
        "efficiency",
    )
    list_filter = ("production_line", "style", "date")

    def efficiency(self, obj):
        efficiency = obj.efficiency_percentage()
        if efficiency < 70:
            color = "red"
        elif efficiency < 90:
            color = "orange"
        else:
            color = "green"
        return format_html('<span style="color: {};">{:.1f}%</span>', color, efficiency)

    efficiency.short_description = "Efficiency"


@admin.register(Style)
class StyleAdmin(BaseModelAdmin):
    list_display = ("style_name", "created_at", "updated_at")
    inlines = [MaterialInline, OrderInline]


@admin.register(Order)
class OrderAdmin(BaseModelAdmin):
    list_display = ("buyer", "season", "style", "order_number", "delivery_date")
    list_filter = ("buyer", "season", "style")
    inlines = [OrderItemInline]


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
    inlines = [QualityCheckInline]


@admin.register(QualityCheck)
class QualityCheckAdmin(BaseModelAdmin):
    list_display = ("scan_event", "status", "defects_list", "created_at", "updated_at")
    list_filter = ("status", "defects")
    filter_horizontal = ("defects",)
    inlines = [ReworkAssignmentInline]

    def defects_list(self, obj):
        return ", ".join([defect.name for defect in obj.defects.all()])

    defects_list.short_description = "Defects"


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
