from django.contrib import admin
from django.utils.html import format_html
from common.admin import BaseModelAdmin, BaseInlineAdmin
from tracker.models import (
    Buyer,
    Season,
    Style,
    MaterialPiece,
    Bundle,
    ProductionLine,
    Scanner,
    ScanEvent,
)


class MaterialPieceInline(BaseInlineAdmin):
    model = MaterialPiece
    extra = 1
    fields = ["name", "qr_image_display"]
    readonly_fields = ["qr_image_display"]

    def qr_image_display(self, obj):
        if obj.pk and obj.qr_image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" width="100" /><br>View QR Code</a>',
                obj.qr_image.url,
                obj.qr_image.url,
            )
        return "QR code will be generated after saving"

    qr_image_display.short_description = "QR Code"


class ScannerInline(BaseInlineAdmin):
    model = Scanner
    extra = 1


# --- MAIN ADMIN CLASSES ---


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
    inlines = [MaterialPieceInline]


@admin.register(MaterialPiece)
class MaterialPieceAdmin(BaseModelAdmin):
    list_display = (
        "style",
        "name",
        "qr_code",
        "qr_image_display",
        "created_at",
        "updated_at",
    )
    list_filter = ("style",)
    readonly_fields = ["qr_code", "qr_image_display"]
    fields = ["style", "name", "qr_code", "qr_image_display"]

    def qr_image_display(self, obj):
        if obj.qr_image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" width="100" /><br>View QR Code</a>',
                obj.qr_image.url,
                obj.qr_image.url,
            )
        return "No QR code available"

    qr_image_display.short_description = "QR Code Image"


@admin.register(Bundle)
class BundleAdmin(BaseModelAdmin):
    list_display = ("name", "qr_code", "qr_image_display", "created_at", "updated_at")
    filter_horizontal = ("pieces",)
    readonly_fields = ["qr_code", "qr_image_display"]
    fields = ["name", "pieces", "qr_code", "qr_image_display"]

    def qr_image_display(self, obj):
        if obj.qr_image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" width="100" /><br>View QR Code</a>',
                obj.qr_image.url,
                obj.qr_image.url,
            )
        return "No QR code available"

    qr_image_display.short_description = "QR Code Image"


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
    list_display = ("scanner", "material_piece", "bundle", "scan_time")
    list_filter = ("scanner", "scan_time")
