import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from tracker.models import MaterialPiece, Bundle, Scanner, ScanEvent


@csrf_exempt
@login_required
def scan_qr(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        qr_data = data.get("qr_data")
        scanner_name = data.get("scanner_name")

        try:
            scanner = Scanner.objects.get(name=scanner_name)
        except Scanner.DoesNotExist:
            return HttpResponse("Scanner not found", status=400)

        if qr_data.startswith("material_piece:"):
            piece_id = qr_data.split(":")[1]
            try:
                piece = MaterialPiece.objects.get(pk=piece_id)
                # Record the scan event for the material piece
                ScanEvent.objects.create(scanner=scanner, material_piece=piece)
                return HttpResponse(
                    f"Material Piece {piece.name} scanned by {scanner.name}"
                )
            except MaterialPiece.DoesNotExist:
                return HttpResponse("Material Piece not found", status=404)
        elif qr_data.startswith("bundle:"):
            bundle_id = qr_data.split(":")[1]
            try:
                bundle = Bundle.objects.get(pk=bundle_id)
                # Record the scan event for the bundle
                ScanEvent.objects.create(scanner=scanner, bundle=bundle)
                return HttpResponse(f"Bundle {bundle.name} scanned by {scanner.name}")
            except Bundle.DoesNotExist:
                return HttpResponse("Bundle not found", status=404)
        else:
            return HttpResponse("Invalid QR code", status=400)
    else:
        return render(request, "tracker/scan_qr.html")


@login_required
def dashboard(request):
    total_pieces = MaterialPiece.objects.count()
    total_bundles = Bundle.objects.count()
    total_scan_events = ScanEvent.objects.count()
    latest_scan_events = ScanEvent.objects.order_by("-scan_time")[:10]

    context = {
        "total_pieces": total_pieces,
        "total_bundles": total_bundles,
        "total_scan_events": total_scan_events,
        "latest_scan_events": latest_scan_events,
    }
    return render(request, "tracker/dashboard.html", context)
