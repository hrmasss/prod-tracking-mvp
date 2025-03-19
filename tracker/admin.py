from django.contrib import admin
from tracker.utils import generate_material_qr_code, render_qr_code
from common.admin import BaseModelAdmin, BaseStackedInline, BaseTabularInline
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
)


class MaterialInline(BaseTabularInline):
    model = Material
    extra = 1


class MaterialPieceInline(BaseTabularInline):
    model = MaterialPiece
    extra = 1
    fields = ["material", "qr_image_display"]
    readonly_fields = ["qr_image_display"]

    def qr_image_display(self, obj):
        return render_qr_code(obj)

    qr_image_display.short_description = "QR Code"

    def save_model(self, request, obj, form, change):
        # Generate QR code if it doesn't exist
        if not obj.qr_code:
            generate_material_qr_code(obj)
        super().save_model(request, obj, form, change)


class ScannerInline(BaseStackedInline):
    model = Scanner
    extra = 1


@admin.register(Buyer)
class BuyerAdmin(BaseModelAdmin):
    list_display = ("name", "created_at", "updated_at")


@admin.register(Season)
class SeasonAdmin(BaseModelAdmin):
    list_display = ("name", "created_at", "updated_at")


@admin.register(Style)
class StyleAdmin(BaseModelAdmin):
    list_display = ("buyer", "season", "style_number", "created_at", "updated_at")
    list_filter = ("buyer", "season")
    inlines = [MaterialInline]


@admin.register(Material)
class MaterialAdmin(BaseModelAdmin):
    list_display = ("style", "name")
    list_filter = ("style",)


@admin.register(MaterialPiece)
class MaterialPieceAdmin(BaseModelAdmin):
    list_display = (
        "material",
        "qr_code",
        "qr_image_display",
        "current_production_line",
        "production_batch",
        "created_at",
        "updated_at",
    )
    list_filter = ("material", "current_production_line", "production_batch")
    readonly_fields = ["qr_code", "qr_image_display"]
    fields = [
        "material",
        "qr_code",
        "qr_image_display",
        "current_production_line",
        "production_batch",
    ]

    def qr_image_display(self, obj):
        return render_qr_code(obj)

    qr_image_display.short_description = "QR Code"


@admin.register(ProductionBatch)
class ProductionBatchAdmin(BaseModelAdmin):
    list_display = ("style", "batch_number", "created_at", "updated_at")
    inlines = [MaterialPieceInline]
    filter_horizontal = ("production_lines",)


@admin.register(ProductionLine)
class ProductionLineAdmin(BaseModelAdmin):
    list_display = ("name", "location", "created_at", "updated_at")
    inlines = [ScannerInline]


@admin.register(Scanner)
class ScannerAdmin(BaseModelAdmin):
    list_display = ("name", "production_line", "created_at", "updated_at")
    list_filter = ("production_line",)


@admin.register(ScanEvent)
class ScanEventAdmin(BaseModelAdmin):
    list_display = ("scanner", "material_piece", "scan_time")
    list_filter = ("scanner", "scan_time")
