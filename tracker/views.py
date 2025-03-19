import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from tracker.models import (
    MaterialPiece,
    Bundle,
    Scanner,
    ScanEvent,
    ProductionBatch,
    ProductionLine,
)
from django.db.models import Count, Q


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
            production_line = scanner.production_line
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
        except MaterialPiece.DoesNotExist:
            pass

        try:
            # Try to find a Bundle
            bundle = Bundle.objects.get(qr_code=qr_data)
        except Bundle.DoesNotExist:
            pass

        if not material_piece and not bundle:
            return HttpResponse("Invalid QR code", status=400)

        # Check if a scan event already exists for this scanner and QR code
        if material_piece:
            existing_scan = ScanEvent.objects.filter(
                scanner=scanner, material_piece=material_piece
            ).exists()
        elif bundle:
            existing_scan = ScanEvent.objects.filter(
                scanner=scanner, bundle=bundle
            ).exists()
        else:
            existing_scan = False

        if existing_scan:
            return HttpResponse("Scan already registered", status=200)

        # Create the ScanEvent
        scan_event = ScanEvent.objects.create(
            scanner=scanner, material_piece=material_piece, bundle=bundle
        )

        # Update MaterialPiece location
        if material_piece:
            material_piece.current_production_line = production_line
            material_piece.save()
            return HttpResponse(
                f"Material Piece {material_piece.name} scanned at {production_line.name}"
            )
        elif bundle:
            # If a bundle is scanned, update the location of all material pieces in the bundle
            for piece in bundle.preset.pieces.all():
                piece.current_production_line = production_line
                piece.save()
            return HttpResponse(f"Bundle {bundle.pk} scanned at {production_line.name}")

    return HttpResponse("Invalid request", status=400)


def dashboard(request):
    production_batches = ProductionBatch.objects.all()
    batch_id = request.GET.get("batch_id")
    selected_batch = None

    if batch_id:
        selected_batch = get_object_or_404(ProductionBatch, pk=batch_id)
        total_pieces = MaterialPiece.objects.filter(style=selected_batch.style).count()
        total_bundles = Bundle.objects.filter(production_batch=selected_batch).count()
        total_scan_events = ScanEvent.objects.count()
        latest_scan_events = ScanEvent.objects.order_by("-scan_time")[:10]

        # Get production line stats
        production_lines = ProductionLine.objects.all()
        production_line_stats = []
        for line in production_lines:
            # Count input pieces
            input_pieces = MaterialPiece.objects.filter(
                current_production_line=line, style=selected_batch.style
            ).count()

            # Count output pieces (check for later scans)
            output_pieces = 0
            pieces_in_line = MaterialPiece.objects.filter(
                current_production_line=line, style=selected_batch.style
            )
            for piece in pieces_in_line:
                later_scan_exists = ScanEvent.objects.filter(
                    material_piece=piece, scan_time__gt=piece.created_at
                ).exists()
                if later_scan_exists:
                    output_pieces += 1

            # Calculate shortage/liability
            shortage_liability = input_pieces - output_pieces

            production_line_stats.append(
                {
                    "line": line,
                    "input_pieces": input_pieces,
                    "output_pieces": output_pieces,
                    "shortage_liability": shortage_liability,
                }
            )
    else:
        total_pieces = 0
        total_bundles = 0
        total_scan_events = 0
        latest_scan_events = []
        production_line_stats = []

    context = {
        "production_batches": production_batches,
        "selected_batch": selected_batch,
        "total_pieces": total_pieces,
        "total_bundles": total_bundles,
        "total_scan_events": total_scan_events,
        "latest_scan_events": latest_scan_events,
        "production_line_stats": production_line_stats,
    }
    return render(request, "tracker/dashboard.html", context)
