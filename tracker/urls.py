from django.urls import path
from tracker.views import scan_qr, dashboard

urlpatterns = [
    path("scan/", scan_qr, name="scan_qr"),
    path("", dashboard, name="dashboard"),
]
