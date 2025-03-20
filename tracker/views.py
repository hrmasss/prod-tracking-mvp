import json
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from tracker.models import (
    MaterialPiece,
    Scanner,
    ScanEvent,
    ProductionBatch,
    ProductionLine,
    QualityCheck,
    Defect,
    ReworkAssignment,
)


def scan_qr(request):
    scanners = Scanner.objects.all()
    return render(request, "tracker/scan_qr.html", {"scanners": scanners})


def scanner_scan(request, scanner_id):
    scanner = get_object_or_404(Scanner, pk=scanner_id)

    # Get defects for QC scanners
    defects = None
    if scanner.type == Scanner.ScannerType.QC:
        defects = Defect.objects.all().order_by("type", "name")

    return render(
        request, "tracker/scanner_scan.html", {"scanner": scanner, "defects": defects}
    )


@csrf_exempt
def scan_qr_data(request):
    if request.method == "POST":
        print(f"Request body: {request.body}")
        data = json.loads(request.body.decode("utf-8"))
        qr_data = data.get("qr_data")
        scanner_name = data.get("scanner_name")

        # For QC scanners, we might get additional data
        quality_status = data.get("quality_status")
        defect_ids = data.get("defect_ids", [])
        rework_notes = data.get("rework_notes")

        try:
            scanner = Scanner.objects.get(name=scanner_name)
            production_line = scanner.production_line
            if not production_line:
                return JsonResponse(
                    {"error": "Scanner is not assigned to a production line."},
                    status=400,
                )
        except Scanner.DoesNotExist:
            return JsonResponse({"error": "Scanner not found"}, status=400)

        try:
            # Try to find a MaterialPiece
            material_piece = MaterialPiece.objects.get(qr_code=qr_data)
        except MaterialPiece.DoesNotExist:
            return JsonResponse({"error": "Invalid QR code"}, status=400)

        # Check if a scan event already exists for this scanner and QR code
        existing_scan = ScanEvent.objects.filter(
            scanner=scanner, material_piece=material_piece
        ).exists()

        if existing_scan:
            return JsonResponse({"message": "Scan already registered"}, status=200)

        # Create the ScanEvent
        scan_event = ScanEvent.objects.create(
            scanner=scanner, material_piece=material_piece
        )

        # Handle different scanner types
        if scanner.type == Scanner.ScannerType.IN:
            # Update MaterialPiece location
            material_piece.current_production_line = production_line
            material_piece.production_flow.add(production_line)
            material_piece.save()

            return JsonResponse(
                {
                    "message": f"Material Piece {material_piece.bundle.material.name} scanned at {production_line.name}",
                    "status": "success",
                }
            )

        elif scanner.type == Scanner.ScannerType.QC:
            # Create quality check record
            if not quality_status:
                return JsonResponse(
                    {"error": "Quality status is required for QC scanners"}, status=400
                )

            quality_check = QualityCheck.objects.create(
                scan_event=scan_event,
                status=quality_status,
                notes=data.get("notes", ""),
            )

            # Add defects if any
            if defect_ids:
                defects = Defect.objects.filter(id__in=defect_ids)
                quality_check.defects.add(*defects)

            # Create rework assignment if status is REWORK
            if quality_status == QualityCheck.QualityStatus.REWORK and rework_notes:
                ReworkAssignment.objects.create(
                    quality_check=quality_check,
                    rework_production_line=production_line,
                    rework_notes=rework_notes,
                )

            return JsonResponse(
                {
                    "message": f"Quality Check completed for {material_piece.bundle.material.name} with status {quality_status}",
                    "status": "success",
                }
            )

        elif scanner.type == Scanner.ScannerType.OUT:
            # Material piece is leaving this production line
            # We don't remove it from production_flow as we want to keep history

            return JsonResponse(
                {
                    "message": f"Material Piece {material_piece.bundle.material.name} completed at {production_line.name}",
                    "status": "success",
                }
            )

    return JsonResponse({"error": "Invalid request"}, status=400)


def dashboard(request):
    production_batches = ProductionBatch.objects.all()
    batch_id = request.GET.get("batch_id")
    selected_batch = None

    if batch_id:
        selected_batch = get_object_or_404(ProductionBatch, pk=batch_id)
        # Get total pieces
        total_pieces = MaterialPiece.objects.filter(
            bundle__production_batch=selected_batch
        ).count()

        # Material breakdown
        material_breakdown = (
            MaterialPiece.objects.filter(bundle__production_batch=selected_batch)
            .values("bundle__material__name")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # Get production line stats
        production_lines = ProductionLine.objects.all()
        production_line_stats = []

        for line in production_lines:
            # Get all scanners for this line
            in_scanners = Scanner.objects.filter(
                production_line=line, type=Scanner.ScannerType.IN
            )
            out_scanners = Scanner.objects.filter(
                production_line=line, type=Scanner.ScannerType.OUT
            )
            qc_scanners = Scanner.objects.filter(
                production_line=line, type=Scanner.ScannerType.QC
            )

            # Count pieces scanned at IN scanners
            input_pieces = (
                ScanEvent.objects.filter(
                    scanner__in=in_scanners,
                    material_piece__bundle__production_batch=selected_batch,
                )
                .values("material_piece")
                .distinct()
                .count()
            )

            # Count pieces scanned at OUT scanners
            output_pieces = (
                ScanEvent.objects.filter(
                    scanner__in=out_scanners,
                    material_piece__bundle__production_batch=selected_batch,
                )
                .values("material_piece")
                .distinct()
                .count()
            )

            # Get QC statistics
            qc_scans = ScanEvent.objects.filter(
                scanner__in=qc_scanners,
                material_piece__bundle__production_batch=selected_batch,
            ).prefetch_related("quality_check")

            # Count by QC status
            accepted_count = 0
            rejected_count = 0
            rework_count = 0

            for scan in qc_scans:
                if hasattr(scan, "quality_check"):
                    if scan.quality_check.status == QualityCheck.QualityStatus.ACCEPTED:
                        accepted_count += 1
                    elif (
                        scan.quality_check.status == QualityCheck.QualityStatus.REJECTED
                    ):
                        rejected_count += 1
                    elif scan.quality_check.status == QualityCheck.QualityStatus.REWORK:
                        rework_count += 1

            # Calculate shortage/liability
            shortage_liability = input_pieces - output_pieces

            # Calculate efficiency if there are input pieces
            efficiency = 0
            if input_pieces > 0:
                efficiency = (output_pieces / input_pieces) * 100

            production_line_stats.append(
                {
                    "line": line,
                    "input_pieces": input_pieces,
                    "output_pieces": output_pieces,
                    "shortage_liability": shortage_liability,
                    "efficiency": efficiency,
                    "accepted_count": accepted_count,
                    "rejected_count": rejected_count,
                    "rework_count": rework_count,
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
