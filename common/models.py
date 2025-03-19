from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from safedelete.models import SafeDeleteModel, HARD_DELETE_NOCASCADE


# --- ABSTRACT BASE MODEL ---


class BaseModel(SafeDeleteModel):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    history = HistoricalRecords(inherit=True)
    _safedelete_policy = HARD_DELETE_NOCASCADE

    class Meta:
        abstract = True