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
        print(f"Scanner {scanner_name} scanned QR code {qr_data}")

        try:
            scanner = Scanner.objects.get(name=scanner_name)
            production_line = scanner.production_line  # Get the production line
            if not production_line:
                return HttpResponse(
                    "Scanner is not assigned to a production line.", status=400
                )
        except Scanner.DoesNotExist:
            return HttpResponse("Scanner not found", status=400)

        material_piece = None
        bundle = None

        try:
            # Try to find a MaterialPiece
            material_piece = MaterialPiece.objects.get(qr_code=qr_data)
            print(
                f"Material Piece {material_piece.name} scanned at {production_line.name}"
            )
        except MaterialPiece.DoesNotExist:
            pass

        try:
            # Try to find a Bundle
            bundle = Bundle.objects.get(qr_code=qr_data)
            print(f"Bundle {bundle.pk} scanned at {production_line.name}")
        except Bundle.DoesNotExist:
            pass

        if not material_piece and not bundle:
            return HttpResponse("Invalid QR code", status=400)

        # Create the ScanEvent
        ScanEvent.objects.create(
            scanner=scanner, material_piece=material_piece, bundle=bundle
        )

        if material_piece:
            return HttpResponse(
                f"Material Piece {material_piece.name} scanned at {production_line.name}"
            )
        elif bundle:
            return HttpResponse(f"Bundle {bundle.pk} scanned at {production_line.name}")

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
