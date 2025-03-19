import os
import qrcode
import hashlib
from io import BytesIO
from django.core.files.base import ContentFile


# --- HELPER FUNCTIONS ---


def material_qr_image_upload_path(instance, filename):
    # Generate path structure: buyer/season/style/
    style = instance.style
    buyer = style.buyer.name.replace(" ", "_")
    season = style.season.name.replace(" ", "_")
    style_number = style.style_number.replace(" ", "_")

    # Create directory structure
    path = f"qr_codes/{buyer}/{season}/{style_number}"
    return os.path.join(path, filename)


def bundle_qr_image_upload_path(instance, filename):
    # For bundles, we'll use a bundles directory
    return f"qr_codes/bundles/{filename}"


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
        filename = f"{instance.name.replace(' ', '_')}_qr.png"

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
    """Generate QR code for a bundle instance with 8-digit numeric code"""
    if instance:
        # Generate the 8-digit numeric code (2 + 7 digits)
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
        filename = f"{instance.name.replace(' ', '_')}_qr.png"

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
