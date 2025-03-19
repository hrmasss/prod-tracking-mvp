import json
from django.db.models import Count
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from tracker.models import (
    MaterialPiece,
    Scanner,
    ScanEvent,
    ProductionBatch,
    ProductionLine,
)


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

        try:
            # Try to find a MaterialPiece
            material_piece = MaterialPiece.objects.get(qr_code=qr_data)
        except MaterialPiece.DoesNotExist:
            return HttpResponse("Invalid QR code", status=400)

        # Check if a scan event already exists for this scanner and QR code
        existing_scan = ScanEvent.objects.filter(
            scanner=scanner, material_piece=material_piece
        ).exists()

        if existing_scan:
            return HttpResponse("Scan already registered", status=200)

        # Create the ScanEvent
        scan_event = ScanEvent.objects.create(
            scanner=scanner, material_piece=material_piece
        )

        # Update MaterialPiece location
        material_piece.current_production_line = production_line
        material_piece.save()
        return HttpResponse(
            f"Material Piece {material_piece.material.name} scanned at {production_line.name}"
        )

    return HttpResponse("Invalid request", status=400)


def dashboard(request):
    production_batches = ProductionBatch.objects.all()
    batch_id = request.GET.get("batch_id")
    selected_batch = None

    if batch_id:
        selected_batch = get_object_or_404(ProductionBatch, pk=batch_id)
        total_pieces = MaterialPiece.objects.filter(
            production_batch=selected_batch
        ).count()

        # Material breakdown
        material_breakdown = (
            MaterialPiece.objects.filter(production_batch=selected_batch)
            .values("material__name")
            .annotate(count=Count("material__name"))
            .order_by("-count")
        )

        # Get production line stats
        production_lines = ProductionLine.objects.all()
        production_line_stats = []
        for line in production_lines:
            # Count input pieces
            input_pieces = MaterialPiece.objects.filter(
                current_production_line=line, production_batch=selected_batch
            ).count()

            # Count output pieces (check for later scans)
            output_pieces = 0
            pieces_in_line = MaterialPiece.objects.filter(
                current_production_line=line, production_batch=selected_batch
            )
            for piece in pieces_in_line:
                # Check if there's a later scan event for this piece
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
        production_line_stats = []
        material_breakdown = []

    context = {
        "production_batches": production_batches,
        "selected_batch": selected_batch,
        "total_pieces": total_pieces,
        "production_line_stats": production_line_stats,
        "material_breakdown": material_breakdown,
    }
    return render(request, "tracker/dashboard.html", context)
