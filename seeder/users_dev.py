from seeder.factories import UserFactory
from users.models import Department, Role
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


def create_superuser():
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin", password="admin", email="admin@test.com"
        )
        print("✅ Superuser 'admin' created.")
    else:
        print("Superuser 'admin' already exists.")


def create_staff_users(num_users=5):
    """
    Creates staff users with view-only permissions for all tracker models.
    """

    # Get all tracker models
    tracker_models = [
        "buyer",
        "season",
        "size",
        "color",
        "style",
        "order",
        "orderitem",
        "materialtype",
        "material",
        "operation",
        "productionline",
        "productionbatch",
        "bundle",
        "materialpiece",
        "scanner",
        "defect",
        "qualitycheck",
        "reworkassignment",
        "scanevent",
        "productiontarget",
    ]

    # Get view permissions for all tracker models
    permissions = Permission.objects.filter(
        codename__startswith="view_",
        content_type__app_label="tracker",
        content_type__model__in=tracker_models,
    )

    for i in range(num_users):
        user = UserFactory.create()
        user.user_permissions.add(*permissions)
        print(f"👤 Staff user '{user.username}' created with view-only permissions.")


def create_departments_and_roles():
    """
    Creates some default departments and roles.
    """
    if not Department.objects.filter(name="Production").exists():
        Department.objects.create(name="Production")
        print("🏢 Department 'Production' created.")
    else:
        print("Department 'Production' already exists.")

    if not Role.objects.filter(name="Operator").exists():
        Role.objects.create(name="Operator")
        print("💼 Role 'Operator' created.")
    else:
        print("Role 'Operator' already exists.")


def seed_users(full=True):
    create_superuser()

    if full:
        create_departments_and_roles()
        create_staff_users()
