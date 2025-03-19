import os


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
