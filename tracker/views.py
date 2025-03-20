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
    Bundle,
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

        # First try to find a Material Piece with the scanned QR code
        material_pieces = []
        try:
            material_piece = MaterialPiece.objects.get(qr_code=qr_data)
            material_pieces = [material_piece]
        except MaterialPiece.DoesNotExist:
            # If not found, try to find a Bundle
            try:
                bundle = Bundle.objects.get(qr_code=qr_data)
                # Get all material pieces from this bundle
                material_pieces = list(bundle.material_pieces.all())
                if not material_pieces:
                    return JsonResponse(
                        {"error": "Bundle found but it has no material pieces"},
                        status=400,
                    )
            except Bundle.DoesNotExist:
                return JsonResponse(
                    {
                        "error": "Invalid QR code - not matching any Material Piece or Bundle"
                    },
                    status=400,
                )

        # Process all material pieces
        processed_count = 0
        for material_piece in material_pieces:
            # Check if a scan event already exists for this scanner and QR code
            existing_scan = ScanEvent.objects.filter(
                scanner=scanner, material_piece=material_piece
            ).exists()

            if existing_scan:
                continue  # Skip this piece if already scanned

            # Create the ScanEvent
            scan_event = ScanEvent.objects.create(
                scanner=scanner, material_piece=material_piece
            )
            processed_count += 1

            # Handle different scanner types
            if scanner.type == Scanner.ScannerType.IN:
                # Update MaterialPiece location
                material_piece.current_production_line = production_line
                material_piece.production_flow.add(production_line)
                material_piece.save()

            elif scanner.type == Scanner.ScannerType.QC:
                # Create quality check record
                if not quality_status:
                    return JsonResponse(
                        {"error": "Quality status is required for QC scanners"},
                        status=400,
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

            # For OUT scanners, we don't need to do anything special other than create the scan event
            # The material_piece.production_flow already keeps track of history

        # Generate appropriate message based on scan result
        if processed_count == 0:
            return JsonResponse(
                {
                    "message": "All pieces in this scan were already processed",
                    "status": "success",
                }
            )

        if len(material_pieces) > 1:
            # Bundle scan
            bundle_name = material_pieces[0].bundle.material.name
            if scanner.type == Scanner.ScannerType.IN:
                message = f"Bundle {bundle_name}: {processed_count} pieces scanned at {production_line.name}"
            elif scanner.type == Scanner.ScannerType.QC:
                message = f"Bundle {bundle_name}: {processed_count} pieces quality checked as {quality_status}"
            else:  # OUT
                message = f"Bundle {bundle_name}: {processed_count} pieces completed at {production_line.name}"
        else:
            # Single piece scan
            piece_name = material_pieces[0].bundle.material.name
            if scanner.type == Scanner.ScannerType.IN:
                message = (
                    f"Material Piece {piece_name} scanned at {production_line.name}"
                )
            elif scanner.type == Scanner.ScannerType.QC:
                message = f"Quality Check completed for {piece_name} with status {quality_status}"
            else:  # OUT
                message = (
                    f"Material Piece {piece_name} completed at {production_line.name}"
                )

        return JsonResponse({"message": message, "status": "success"})

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
