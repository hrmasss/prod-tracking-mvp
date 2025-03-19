import qrcode
from io import BytesIO
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline  # Import TabularInline
from django.core.files.base import ContentFile
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


# --- INLINE ADMIN CLASSES ---


class MaterialPieceInline(TabularInline):
    model = MaterialPiece
    extra = 1


class ScannerInline(TabularInline):
    model = Scanner
    extra = 1


# --- MAIN ADMIN CLASSES ---


@admin.register(Buyer)
class BuyerAdmin(ModelAdmin):
    list_display = ("name", "created_at", "updated_at")


@admin.register(Season)
class SeasonAdmin(ModelAdmin):
    list_display = ("name", "created_at", "updated_at")


@admin.register(Style)
class StyleAdmin(ModelAdmin):
    list_display = ("buyer", "season", "style_number", "created_at", "updated_at")
    list_filter = ("buyer", "season")
    inlines = [MaterialPieceInline]


@admin.register(MaterialPiece)
class MaterialPieceAdmin(ModelAdmin):
    list_display = ("style", "name", "qr_code", "created_at", "updated_at")
    list_filter = ("style",)

    def save_model(self, request, obj, form, change):
        # Generate QR code if it doesn't exist
        if not obj.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr_data = f"material_piece:{obj.id}"
            qr.add_data(qr_data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_code_image = ContentFile(
                buffer.getvalue(), f"material_piece_{obj.id}.png"
            )

            obj.qr_code = f"material_piece_{obj.id}.png"
            # TODO: Save the image to a file storage
            # obj.qr_code.save(f"material_piece_{obj.id}.png", qr_code_image, save=False)

        super().save_model(request, obj, form, change)


@admin.register(Bundle)
class BundleAdmin(ModelAdmin):
    list_display = ("name", "qr_code", "created_at", "updated_at")
    filter_horizontal = ("pieces",)

    def save_model(self, request, obj, form, change):
        # Generate QR code if it doesn't exist
        if not obj.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr_data = f"bundle:{obj.id}"
            qr.add_data(qr_data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_code_image = ContentFile(buffer.getvalue(), f"bundle_{obj.id}.png")

            obj.qr_code = f"bundle_{obj.id}.png"
            # TODO: Save the image to a file storage
            # obj.qr_code.save(f"bundle_{obj.id}.png", qr_code_image, save=False)

        super().save_model(request, obj, form, change)


@admin.register(ProductionLine)
class ProductionLineAdmin(ModelAdmin):
    list_display = ("name", "location", "created_at", "updated_at")
    inlines = [ScannerInline]


@admin.register(Scanner)
class ScannerAdmin(ModelAdmin):
    list_display = ("name", "production_line", "created_at", "updated_at")
    list_filter = ("production_line",)


@admin.register(ScanEvent)
class ScanEventAdmin(ModelAdmin):
    list_display = ("scanner", "material_piece", "bundle", "scan_time")
    list_filter = ("scanner", "scan_time")
