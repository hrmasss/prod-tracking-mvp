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
    for _ in range(5):
        SeasonFactory.create()
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
        "Fabric",
        "Lining",
        "Zipper",
        "Button",
        "Thread",
        "Label",
        "Interlining",
        "Padding",
        "Buckle",
        "Snap",
        "Velcro",
        "Elastic",
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


def create_styles(num_styles=10):
    for _ in range(num_styles):
        StyleFactory.create()
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
    create_styles()

    if full:
        create_orders()
        create_order_items()
        create_materials()
        create_production_batches()
        create_bundles()
        create_material_pieces()
