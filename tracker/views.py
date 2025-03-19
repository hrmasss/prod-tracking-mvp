import json
from django.http import HttpResponse
from django.db.models import Count, Min, F, Q
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
            # Get all scanners for the current production line
            in_scanners = Scanner.objects.filter(
                production_line=line, type=Scanner.ScannerType.IN
            )

            # Count unique material pieces that have their FIRST scan event on this line
            input_pieces = (
                MaterialPiece.objects.filter(production_batch=selected_batch)
                .filter(
                    scan_events__scanner__in=in_scanners
                )  # Scanned by an IN scanner on this line
                .annotate(first_scan=Min("scan_events__scan_time"))
                .filter(scan_events__scan_time=F("first_scan"))
                .distinct()
                .count()
            )

            # Count unique material pieces that have a scan event on a DIFFERENT production line AFTER being scanned on this line
            output_pieces = (
                MaterialPiece.objects.filter(production_batch=selected_batch)
                .filter(
                    scan_events__scanner__production_line=line
                )  # Scanned on this line at some point
                .annotate(
                    first_scan_on_line=Min(
                        "scan_events__scan_time",
                        filter=Q(scan_events__scanner__production_line=line),
                    )
                )  # Find the first scan on this line
                .filter(
                    scan_events__scan_time__gt=F("first_scan_on_line")
                )  # Filter for scans AFTER the first scan on this line
                .exclude(
                    scan_events__scanner__production_line=line
                )  # Exclude scans on the current line
                .distinct()
                .count()
            )

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
