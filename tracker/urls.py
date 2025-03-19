from django.urls import path
from tracker.views import scan_qr, scanner_scan, dashboard, scan_qr_data

urlpatterns = [
    path("scan/", scan_qr, name="scan_qr"),
    path("scan/<int:scanner_id>/", scanner_scan, name="scanner_scan"),
    path("scan_data/", scan_qr_data, name="scan_qr_data"),
    path("", dashboard, name="dashboard"),
]
