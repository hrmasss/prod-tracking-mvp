import os
import qrcode
import hashlib
from io import BytesIO
from django.utils.html import format_html
from django.core.files.base import ContentFile


# --- HELPER FUNCTIONS ---


def material_qr_image_upload_path(instance, filename):
    # Generate path structure: buyer/season/style/
    style = instance.bundle.material.style
    buyer = style.buyer.name.replace(" ", "_")
    season = style.season.name.replace(" ", "_")
    style_name = style.style_name.replace(" ", "_")

    # Create directory structure
    path = f"qr_codes/{buyer}/{season}/{style_name}"
    return os.path.join(path, filename)


def bundle_qr_image_upload_path(instance, filename):
    # Generate path structure: buyer/season/style/
    style = instance.material.style
    buyer = style.buyer.name.replace(" ", "_")
    season = style.season.name.replace(" ", "_")
    style_name = style.style_name.replace(" ", "_")

    # Create directory structure
    path = f"qr_codes/{buyer}/{season}/{style_name}/bundles"
    return os.path.join(path, filename)


def generate_numeric_code_for_qr(instance_id, prefix):
    """
    Generate a unique 8-digit numeric code
    - prefix: 1 for material pieces, 2 for bundles
    - remaining digits: padded instance_id or hashed value if too large
    """
    # Convert instance_id to string
    id_str = str(instance_id)

    # If ID is already too long, use a hash approach
    if len(id_str) > 7:
        # Create a hash of the ID and take the first 7 digits
        hash_object = hashlib.md5(id_str.encode())
        hash_hex = hash_object.hexdigest()
        # Convert hex to decimal and take first 7 digits
        hash_decimal = str(int(hash_hex, 16))
        id_portion = hash_decimal[:7]
    else:
        # Pad with zeroes to ensure 7 digits
        id_portion = id_str.zfill(7)

    # Combine prefix and ID portion
    return f"{prefix}{id_portion}"


# --- QR CODE GENERATION ---


def generate_material_qr_code(instance):
    """Generate QR code for a material piece instance with 8-digit numeric code"""
    if instance:
        # Generate the 8-digit numeric code (1 + 7 digits)
        numeric_code = generate_numeric_code_for_qr(instance.id, prefix="1")
        instance.qr_code = numeric_code

        # Generate the QR image
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(numeric_code)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")

        # Create a unique filename
        filename = f"{instance.qr_code}.png"

        # Save the image to the ImageField
        instance.qr_image.save(
            filename,
            ContentFile(buffer.getvalue()),
            save=False,
        )

        # Now save the model with both the code and image updated
        instance.save(update_fields=["qr_code", "qr_image"])
        return True
    return False


def generate_bundle_qr_code(instance):
    """Generate QR code for a bundle instance"""
    if instance:
        # Generate the 8-digit numeric code (2 + 6 digits)
        numeric_code = generate_numeric_code_for_qr(instance.id, prefix="2")
        instance.qr_code = numeric_code

        # Generate the QR image
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(numeric_code)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")

        # Create a unique filename
        filename = f"{instance.qr_code}.png"

        # Save the image to the ImageField
        instance.qr_image.save(
            filename,
            ContentFile(buffer.getvalue()),
            save=False,
        )

        # Now save the model with both the code and image updated
        instance.save(update_fields=["qr_code", "qr_image"])
        return True
    return False


# --- ADMIN UTILITIES ---


def render_qr_code(obj):
    if obj.qr_image:
        filename = "material_piece"
        if hasattr(obj, "bundle"):
            filename = f"{obj.bundle.material.style.buyer.name}_{obj.bundle.material.style.season.name}_{obj.bundle.material.style.style_name}_{obj.bundle.material.name}_{obj.bundle.size}".replace(
                " ", "_"
            )
        else:
            filename = str(obj.pk)

        return format_html(
            '<div style="display: flex; flex-direction: column; align-items: flex-start;">'
            "<div>QR Code: {}</div>"
            '<div style="display: flex; align-items: center;">'
            '<a href="{}" target="_blank"><img src="{}" width="100" /></a>'
            '<div style="margin-left: 10px;">'
            '<a href="{}" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2" download="{}.png">Download</a>'
            '<button onclick="printQrCode(\'{}\')" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Print</button>'
            "</div>"
            "</div>"
            "<script>"
            "function printQrCode(imageUrl) {{"
            "  const printWindow = window.open('', '_blank');"
            "  printWindow.document.write('<html><head><title>Print QR Code</title></head><body>');"
            "  printWindow.document.write('<img src=\\\"' + imageUrl + '\\\" style=\\\"max-width: 100%;\\\">');"
            "  printWindow.document.write('</body></html>');"
            "  printWindow.document.close();"
            "  printWindow.focus();"
            "  printWindow.print();"
            "  printWindow.close();"
            "}}"
            "</script>"
            "</div>",
            obj.qr_code,
            obj.qr_image.url,
            obj.qr_image.url,
            obj.qr_image.url,
            filename,
            obj.qr_image.url,
        )
    return "No QR code available"


def render_combined_qr_codes(pieces):
    qr_code_images = []
    for piece in pieces:
        if piece.qr_image:
            qr_code_images.append(
                f'<img src="{piece.qr_image.url}" style="width: 100px; margin: 5px;" />'
            )
        else:
            qr_code_images.append("<div>No QR code available</div>")

    # Combine all QR codes into a single HTML page
    combined_html = f"""
    <html>
    <head>
        <title>Combined QR Codes</title>
        <style>
            body {{
                display: flex;
                flex-wrap: wrap;
                justify-content: flex-start;
                align-items: flex-start;
            }}
            img {{
                width: 200px;
                height: 200px;
                margin: 5px;
            }}
        </style>
    </head>
    <body>
        {''.join(qr_code_images)}
    </body>
    </html>
    """

    return format_html(
        f'<iframe srcdoc="{combined_html}" width="100%" height="500px"></iframe>'
    )
