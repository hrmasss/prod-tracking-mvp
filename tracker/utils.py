import os
import qrcode
import hashlib
from io import BytesIO
from django.utils.html import format_html
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile


# --- HELPER FUNCTIONS ---


def material_qr_image_upload_path(instance, filename):
    # Generate path structure: buyer/season/style/
    bundle = instance.bundle
    buyer = bundle.production_batch.order.buyer.name.replace(" ", "_")
    season = bundle.production_batch.order.season.name.replace(" ", "_")
    style_name = bundle.production_batch.order.style.name.replace(" ", "_")

    # Create directory structure
    path = f"qr_codes/{buyer}/{season}/{style_name}"
    return os.path.join(path, filename)


def bundle_qr_image_upload_path(instance, filename):
    # Generate path structure: buyer/season/style/
    production_batch = instance.production_batch
    buyer = production_batch.order.buyer.name.replace(" ", "_")
    season = production_batch.order.season.name.replace(" ", "_")
    style_name = production_batch.order.style.name.replace(" ", "_")

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
        qr_img = qr.make_image(fill_color="black", back_color="white").convert(
            "RGB"
        )  # Convert to RGB

        # Fetch additional details
        style_name = instance.bundle.production_batch.order.style.name
        size_name = instance.bundle.size.name if instance.bundle.size else "N/A"
        color_name = instance.bundle.color.name if instance.bundle.color else "N/A"
        batch_number = instance.bundle.production_batch.batch_number or "N/A"
        season_name = instance.bundle.production_batch.order.season.name
        buyer_name = instance.bundle.production_batch.order.buyer.name
        material_type = instance.bundle.material.material_type.name
        material_name = instance.bundle.material.name

        # Prepare text labels
        labels = [
            f"Buyer: {buyer_name}",
            f"Season: {season_name}",
            f"Style: {style_name}",
            f"Size: {size_name}",
            f"Color: {color_name}",
            f"Batch: {batch_number}",
            f"Material Type: {material_type}",
            f"Material Name: {material_name}",
        ]

        # --- Create a combined image ---
        label_width = 300  # Increased width for more text
        qr_width, qr_height = qr_img.size
        img_height = qr_height + 30  # Increased space for the code below
        img_width = label_width + qr_width  # Labels + QR code

        # Create a new image with white background
        combined_img = Image.new("RGB", (img_width, img_height), "white")
        d = ImageDraw.Draw(combined_img)

        # Load a font (adjust path as necessary)
        try:
            font = ImageFont.truetype("arial.ttf", 18)  # Increased font size
        except IOError:
            font = ImageFont.load_default()  # If Arial is not available

        # Add labels to the left
        x_offset = 30
        y_offset = 40
        line_height = 25
        for label in labels:
            d.text((x_offset, y_offset), label, fill="black", font=font)
            y_offset += line_height

        # Paste the QR code
        combined_img.paste(qr_img, (label_width, 0))

        # Add the numeric code below the QR code
        bbox = d.textbbox((0, 0), numeric_code, font=font)
        code_width = bbox[2] - bbox[0]
        code_height = bbox[3] - bbox[1]
        code_x = label_width + (qr_width - code_width) // 2
        code_y = qr_height - 20
        d.text((code_x, code_y), numeric_code, fill="black", font=font)

        buffer = BytesIO()
        combined_img.save(buffer, format="PNG")

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
        qr_img = qr.make_image(fill_color="black", back_color="white").convert(
            "RGB"
        )  # Convert to RGB

        # Fetch additional details
        style_name = instance.production_batch.order.style.name
        size_name = instance.size.name if instance.size else "N/A"
        color_name = instance.color.name if instance.color else "N/A"
        batch_number = instance.production_batch.batch_number or "N/A"
        season_name = instance.production_batch.order.season.name
        buyer_name = instance.production_batch.order.buyer.name

        # Prepare text labels
        labels = [
            f"Buyer: {buyer_name}",
            f"Season: {season_name}",
            f"Style: {style_name}",
            f"Size: {size_name}",
            f"Color: {color_name}",
            f"Batch: {batch_number}",
            f"Bundle ID: {instance.id}",
        ]

        # --- Create a combined image ---
        label_width = 250  # Increased width for more text
        qr_width, qr_height = qr_img.size
        img_height = qr_height + 30  # Increased space for the code below
        img_width = label_width + qr_width  # Labels + QR code

        # Create a new image with white background
        combined_img = Image.new("RGB", (img_width, img_height), "white")
        d = ImageDraw.Draw(combined_img)

        # Load a font (adjust path as necessary)
        try:
            font = ImageFont.truetype("arial.ttf", 18)  # Increased font size
        except IOError:
            font = ImageFont.load_default()  # If Arial is not available

        # Add labels to the left
        x_offset = 15  # Added horizontal offset/padding
        y_offset = 15  # Increased vertical offset/padding
        line_height = 25  # Increased line height for better spacing
        for label in labels:
            d.text((x_offset, y_offset), label, fill="black", font=font)
            y_offset += line_height

        # Paste the QR code
        combined_img.paste(qr_img, (label_width, 0))

        # Add the numeric code below the QR code
        bbox = d.textbbox((0, 0), numeric_code, font=font)
        code_width = bbox[2] - bbox[0]
        code_height = bbox[3] - bbox[1]
        code_x = label_width + (qr_width - code_width) // 2
        code_y = qr_height + 5  # Adjust position of the code
        d.text((code_x, code_y), numeric_code, fill="black", font=font)

        buffer = BytesIO()
        combined_img.save(buffer, format="PNG")

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
        filename = f"{obj.qr_code}"

        # Create HTML content for the iframe
        iframe_html = f"""
        <html>
        <head>
            <title>Print QR Code</title>
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}
                img {{
                    max-width: 100%;
                    max-height: 100%;
                }}
            </style>
        </head>
        <body>
            <img src="{obj.qr_image.url}">
        </body>
        </html>
        """

        return format_html(
            '<div style="display: flex; flex-direction: column; align-items: flex-start;">'
            '<div style="display: flex; align-items: center;">'
            '<a href="{}" target="_blank"><img src="{}" width="200" /></a>'
            '<div style="margin-left: 10px;">'
            '<a href="{}" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2" download="{}">Download</a>'
            '<button type="button" onclick="printSingleQrCode(\'qr-iframe-{}\')" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Print</button>'
            "</div>"
            "</div>"
            '<iframe id="qr-iframe-{}" srcdoc="{}" style="display:none;" width="0" height="0"></iframe>'
            "<script>"
            "function printSingleQrCode(iframeId) {{"
            "  var iframe = document.getElementById(iframeId);"
            "  iframe.contentWindow.focus();"
            "  iframe.contentWindow.print();"
            "}}"
            "</script>"
            "</div>",
            obj.qr_image.url,  # View URL
            obj.qr_image.url,  # Image source URL
            obj.qr_image.url,  # Download URL
            filename + ".png",  # Download filename
            obj.id,  # Unique iframe ID based on object ID
            obj.id,  # Same unique ID for the iframe
            iframe_html,  # HTML content for the iframe
        )
    return "No QR code available"


def render_combined_qr_codes(pieces):
    qr_code_images = []
    for piece in pieces:
        if piece.qr_image:
            qr_code_images.append(
                f'<img src="{piece.qr_image.url}" style="width: 200px; height: 200px; margin: 5px;" />'
            )
        else:
            qr_code_images.append("<div>No QR code available</div>")

    # Combine all QR codes into a single HTML page
    combined_html = f"""
    <html>
    <head>
        <title>Combined QR Codes</title>
        <style>
            @media print {{
                body {{
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: flex-start;
                    align-items: flex-start;
                }}
            }}
            body {{
                display: none;
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
        """
        <button type="button" onclick="printCombinedQrCodes()" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Print All Pieces</button>
        <iframe id="qrCodeFrame" srcdoc="{}" width="0" height="0" style="display:none;"></iframe>
        <script>
            function printCombinedQrCodes() {{
                var qrCodeFrame = document.getElementById('qrCodeFrame');
                qrCodeFrame.contentWindow.focus();
                qrCodeFrame.contentWindow.print();
            }}
        </script>
        """,
        combined_html,
    )
