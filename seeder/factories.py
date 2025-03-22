import factory
import factory.fuzzy
from users import models as users_models
from tracker import models as tracker_models


class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = users_models.Department
        django_get_or_create = ("name",)

    name = factory.fuzzy.FuzzyChoice(["HR", "Accounts", "Commercial", "Management"])


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = users_models.Role
        django_get_or_create = ("name",)

    name = factory.fuzzy.FuzzyChoice(["Manager", "Officer", "Executive"])


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = users_models.User
        django_get_or_create = ("username", "email")

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_staff = True
    is_active = True
    department = factory.SubFactory(DepartmentFactory)


class BuyerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = tracker_models.Buyer
        django_get_or_create = ("name",)

    name = factory.fuzzy.FuzzyChoice(
        ["Hugo Boss", "Cecil", "Macy's", "Marc O'Polo", "Zara", "H&M"]
    )


class SeasonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = tracker_models.Season
        django_get_or_create = ("name",)

    name = factory.fuzzy.FuzzyChoice(["Summer", "Fall", "Winter", "Spring"])


class SizeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = tracker_models.Size
        django_get_or_create = ("name",)

    name = factory.fuzzy.FuzzyChoice(["XS", "S", "M", "L", "XL", "XXL", "One Size"])


class ColorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = tracker_models.Color
        django_get_or_create = ("name",)

    name = factory.fuzzy.FuzzyChoice(
        ["Black", "White", "Red", "Blue", "Green", "Gray", "Navy", "Beige"]
    )


class StyleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = tracker_models.Style

    name = factory.fuzzy.FuzzyChoice(["BOCO", "BERO", "BODI", "MEROS"])


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = tracker_models.Order

    buyer = factory.SubFactory(BuyerFactory)
    season = factory.SubFactory(SeasonFactory)
    style = factory.SubFactory(StyleFactory)
    order_number = factory.Faker("ean", length=13)
    delivery_date = factory.Faker("future_date")


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = tracker_models.OrderItem

    order = factory.SubFactory(OrderFactory)
    size = factory.SubFactory(SizeFactory)
    color = factory.SubFactory(ColorFactory)
    quantity = factory.fuzzy.FuzzyInteger(10, 1000)


class MaterialTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = tracker_models.MaterialType
        django_get_or_create = ("name",)

    name = factory.fuzzy.FuzzyChoice(
        [
            "Hood",
            "Sleeve",
            "Zipper",
            "Interlining",
            "Padding",
        ]
    )


class MaterialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = tracker_models.Material

    name = factory.Faker("word")
    material_type = factory.SubFactory(MaterialTypeFactory)
    unit = factory.fuzzy.FuzzyChoice(["meters", "pcs", "yards"])
    color = factory.SubFactory(ColorFactory)


class OperationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = tracker_models.Operation
        django_get_or_create = ("name",)

    name = factory.Faker("word")
    type = factory.fuzzy.FuzzyChoice(tracker_models.Operation.OperationCategory.values)
    sequence = factory.fuzzy.FuzzyInteger(0, 10)


class ProductionLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = tracker_models.ProductionLine
        django_get_or_create = ("name",)

    name = factory.LazyAttribute(
        lambda _: f"{factory.fuzzy.FuzzyChoice(tracker_models.Operation.OperationCategory.values).fuzz()} - {factory.fuzzy.FuzzyInteger(0, 10).fuzz()}"
    )
    operation_type = factory.fuzzy.FuzzyChoice(
        tracker_models.Operation.OperationCategory.values
    )
    location = factory.fuzzy.FuzzyChoice(["8th Floor", "9th Floor"])


class ProductionBatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = tracker_models.ProductionBatch

    order = factory.SubFactory(OrderFactory)
    batch_number = factory.Faker("ean", length=8)


class BundleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = tracker_models.Bundle

    production_batch = factory.SubFactory(ProductionBatchFactory)
    material = factory.SubFactory(MaterialFactory)
    size = factory.SubFactory(SizeFactory)
    color = factory.SubFactory(ColorFactory)
    quantity = factory.fuzzy.FuzzyInteger(1, 10)


class MaterialPieceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = tracker_models.MaterialPiece

    bundle = factory.SubFactory(BundleFactory)


class ScannerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = tracker_models.Scanner

    name = factory.Sequence(lambda n: f"Scanner {n}")
    production_line = factory.SubFactory(ProductionLineFactory)
    type = factory.fuzzy.FuzzyChoice(tracker_models.Scanner.ScannerType.values)


class DefectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = tracker_models.Defect

    name = factory.Sequence(lambda n: f"Defect {n}")
    type = factory.fuzzy.FuzzyChoice(tracker_models.Operation.OperationCategory.values)
    severity_level = factory.fuzzy.FuzzyInteger(1, 3)
