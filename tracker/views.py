import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from tracker.models import MaterialPiece, Bundle, Scanner, ScanEvent


def scan_qr(request):
    scanners = Scanner.objects.all()
    return render(request, "tracker/scan_qr.html", {"scanners": scanners})


def scanner_scan(request, scanner_id):
    scanner = get_object_or_404(Scanner, pk=scanner_id)
    return render(request, "tracker/scanner_scan.html", {"scanner": scanner})


@csrf_exempt
def scan_qr_data(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        qr_data = data.get("qr_data")
        scanner_name = data.get("scanner_name")

        try:
            scanner = Scanner.objects.get(name=scanner_name)
        except Scanner.DoesNotExist:
            return HttpResponse("Scanner not found", status=400)

        if qr_data.startswith("1"):
            try:
                piece = MaterialPiece.objects.get(qr_code=qr_data)
                ScanEvent.objects.create(scanner=scanner, material_piece=piece)
                return HttpResponse(
                    f"Material Piece {piece.name} scanned by {scanner.name}"
                )
            except MaterialPiece.DoesNotExist:
                return HttpResponse("Material Piece not found", status=404)
        elif qr_data.startswith("2"):
            try:
                bundle = Bundle.objects.get(qr_code=qr_data)
                ScanEvent.objects.create(scanner=scanner, bundle=bundle)
                return HttpResponse(f"Bundle {bundle.pk} scanned by {scanner.name}")
            except Bundle.DoesNotExist:
                return HttpResponse("Bundle not found", status=404)
        else:
            return HttpResponse("Invalid QR code", status=400)
    return HttpResponse("Invalid request", status=400)


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
