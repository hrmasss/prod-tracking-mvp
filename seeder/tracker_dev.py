from tracker.models import ProductionLine, Scanner
from seeder.factories import (
    BuyerFactory,
    SeasonFactory,
    SizeFactory,
    ColorFactory,
    StyleFactory,
    OrderFactory,
    OrderItemFactory,
    MaterialTypeFactory,
    MaterialFactory,
    OperationFactory,
    ProductionLineFactory,
    ProductionBatchFactory,
    BundleFactory,
    MaterialPieceFactory,
    ScannerFactory,
    DefectFactory,
)


def create_buyers():
    buyers = [
        "Hugo Boss",
        "Cecil",
        "Macy's",
        "Marc O'Polo",
        "Zara",
        "H&M",
        "ASOS",
    ]
    for buyer in buyers:
        BuyerFactory.create(name=buyer)
    print("🛍️  Buyers created.")


def create_seasons():
    seasons = ["Summer 2023", "Fall 2023", "Winter 2023", "Spring 2024", "Summer 2024"]
    for season in seasons:
        SeasonFactory.create(name=season)
    print("📅 Seasons created.")


def create_sizes():
    sizes = ["XS", "S", "M", "L", "XL", "XXL", "30", "32", "34", "36", "38", "40"]
    for size in sizes:
        SizeFactory.create(name=size)
    print("📏 Sizes created.")


def create_colors():
    colors = [
        "Black",
        "White",
        "Red",
        "Blue",
        "Green",
        "Gray",
        "Navy",
        "Beige",
        "Brown",
        "Yellow",
        "Orange",
        "Purple",
    ]
    for color in colors:
        ColorFactory.create(name=color)
    print("🎨 Colors created.")


def create_material_types():
    material_types = [
        "Collar",
        "Hood",
        "Sleeve",
        "Lining",
        "Zipper",
        "Button",
        "Thread",
        "Label",
        "Interlining",
        "Padding",
        "Buckle",
        "Pocket",
        "Cuff",
        "Body",
        "Back Panel",
        "Front Panel",
    ]
    for material_type in material_types:
        MaterialTypeFactory.create(name=material_type)
    print("🧵 Material Types created.")


def create_operations():
    operations = [
        {"name": "Cutting", "type": "CUTTING", "sequence": 1},
        {"name": "Sewing", "type": "SEWING", "sequence": 2},
        {"name": "Finishing", "type": "FINISHING", "sequence": 3},
        {"name": "Packing", "type": "PACKING", "sequence": 4},
        {"name": "Quilting", "type": "QUILTING", "sequence": 5},
        {"name": "Downfilling", "type": "DOWNFILLING", "sequence": 6},
    ]
    for operation in operations:
        OperationFactory.create(**operation)
    print("⚙️  Operations created.")


def create_production_lines():
    production_lines = [
        {
            "name": "Cutting Line 1",
            "operation_type": "CUTTING",
            "location": "8th Floor - A",
        },
        {
            "name": "Finishing Line 1",
            "operation_type": "FINISHING",
            "location": "8th Floor - B",
        },
        {
            "name": "Sewing Line 1",
            "operation_type": "SEWING",
            "location": "8th Floor - C",
        },
        {
            "name": "Sewing Line 2",
            "operation_type": "SEWING",
            "location": "8th Floor - C",
        },
        {
            "name": "Sewing Line 3",
            "operation_type": "SEWING",
            "location": "8th Floor - C",
        },
        {
            "name": "Sewing Line 4",
            "operation_type": "SEWING",
            "location": "8th Floor - C",
        },
        {
            "name": "Sewing Line 5",
            "operation_type": "SEWING",
            "location": "8th Floor - C",
        },
        {
            "name": "Sewing Line 6",
            "operation_type": "SEWING",
            "location": "8th Floor - C",
        },
        {
            "name": "Sewing Line 7",
            "operation_type": "SEWING",
            "location": "8th Floor - C",
        },
        {
            "name": "Downfilling Line 1",
            "operation_type": "DOWNFILLING",
            "location": "8th Floor - D",
        },
        {
            "name": "Quilting Line 1",
            "operation_type": "QUILTING",
            "location": "8th Floor - E",
        },
    ]
    for production_line in production_lines:
        ProductionLineFactory.create(**production_line)
    print("🏭 Production Lines created.")


def create_scanners():
    # Create 2 scanners (IN and QC) for each production line
    production_lines = ProductionLine.objects.all()

    for line in production_lines:
        # Create IN scanner
        ScannerFactory.create(
            name=f"{line.name} - Input",
            production_line=line,
            type=Scanner.ScannerType.IN,
        )

        # Create QC scanner
        ScannerFactory.create(
            name=f"{line.name} - QC", production_line=line, type=Scanner.ScannerType.QC
        )

    print("🔍 Scanners created.")


def create_defects():
    defects = [
        # CUTTING defects
        {"name": "Uneven Cut", "type": "CUTTING", "severity_level": 2},
        {"name": "Wrong Size Cut", "type": "CUTTING", "severity_level": 3},
        {"name": "Damaged Material", "type": "CUTTING", "severity_level": 3},
        # SEWING defects
        {"name": "Broken Stitch", "type": "SEWING", "severity_level": 2},
        {"name": "Puckering", "type": "SEWING", "severity_level": 1},
        {"name": "Skipped Stitch", "type": "SEWING", "severity_level": 2},
        {"name": "Uneven Seam", "type": "SEWING", "severity_level": 1},
        {"name": "Raw Edge Visible", "type": "SEWING", "severity_level": 2},
        # FINISHING defects
        {"name": "Button Missing", "type": "FINISHING", "severity_level": 1},
        {"name": "Button Loose", "type": "FINISHING", "severity_level": 1},
        {"name": "Wrong Button", "type": "FINISHING", "severity_level": 2},
        {"name": "Zipper Not Working", "type": "FINISHING", "severity_level": 3},
        # PACKING defects
        {"name": "Wrong Label", "type": "PACKING", "severity_level": 2},
        {"name": "Missing Tag", "type": "PACKING", "severity_level": 1},
        # QUILTING defects
        {"name": "Uneven Quilting", "type": "QUILTING", "severity_level": 2},
        {"name": "Irregular Pattern", "type": "QUILTING", "severity_level": 2},
        # DOWNFILLING defects
        {"name": "Insufficient Fill", "type": "DOWNFILLING", "severity_level": 3},
        {"name": "Overfilled", "type": "DOWNFILLING", "severity_level": 2},
        {
            "name": "Uneven Fill Distribution",
            "type": "DOWNFILLING",
            "severity_level": 2,
        },
    ]

    for defect in defects:
        DefectFactory.create(**defect)

    print("❌ Defects created.")


def create_styles(num_styles=10):
    style_names = [
        "BOCO",
        "BERO",
        "BODI",
        "MEROS",
        "TIMO",
        "CLARA",
        "LIAN",
        "PARKER",
        "JORDAN",
        "ALEX",
    ]

    for i in range(min(num_styles, len(style_names))):
        StyleFactory.create(name=style_names[i])

    print(f"👕 {num_styles} Styles created.")


def create_orders(num_orders=5):
    for _ in range(num_orders):
        OrderFactory.create()
    print(f"🧾 {num_orders} Orders created.")


def create_order_items(num_order_items=20):
    for _ in range(num_order_items):
        OrderItemFactory.create()
    print(f"📦 {num_order_items} Order Items created.")


def create_materials(num_materials=20):
    for _ in range(num_materials):
        MaterialFactory.create()
    print(f"🧱 {num_materials} Materials created.")


def create_production_batches(num_batches=5):
    for _ in range(num_batches):
        ProductionBatchFactory.create()
    print(f"🚧 {num_batches} Production Batches created.")


def create_bundles(num_bundles=20):
    for _ in range(num_bundles):
        BundleFactory.create()
    print(f"묶음 {num_bundles} Bundles created.")


def create_material_pieces(num_pieces=50):
    for _ in range(num_pieces):
        MaterialPieceFactory.create()
    print(f"🧩 {num_pieces} Material Pieces created.")


def seed_tracker_data(full=False):
    create_buyers()
    create_seasons()
    create_sizes()
    create_colors()
    create_material_types()
    create_operations()
    create_production_lines()
    create_scanners() 
    create_defects()
    create_styles()

    if full:
        create_orders()
        create_order_items()
        create_materials()
        create_production_batches()
        create_bundles()
        create_material_pieces()
