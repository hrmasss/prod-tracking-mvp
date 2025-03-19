from django.dispatch import receiver
from django.db.models.signals import post_save
from tracker.models import MaterialPiece
from tracker.utils import generate_material_qr_code


# --- QR CODE GENERATION SIGNALS ---


@receiver(post_save, sender=MaterialPiece)
def material_piece_post_save(sender, instance, created, **kwargs):
    """Handle automatic QR code generation after save"""
    if created or not instance.qr_code:
        generate_material_qr_code(instance)
