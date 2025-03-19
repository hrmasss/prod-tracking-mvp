from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.models import Group
from users.models import User, Department, Role
from unfold.forms import AdminPasswordChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.forms import (
    DepartmentAdminForm,
    RoleAdminForm,
    UserChangeForm,
    UserCreationForm,
)


# --- UNREGISTER DEFAULT ADMIN CLASSES ---


admin.site.unregister(Group)


# --- REGISTER ADMIN CLASSES ---


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("username", "email", "first_name", "last_name", "department")
    list_filter = ("department",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "department", "roles")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    filter_horizontal = ("roles", "user_permissions")


@admin.register(Department)
class DepartmentAdmin(ModelAdmin):
    form = DepartmentAdminForm
    filter_horizontal = ("permissions",)
    list_display = ("name",)


@admin.register(Role)
class RoleAdmin(ModelAdmin):
    form = RoleAdminForm
    filter_horizontal = ("permissions",)
    list_display = ("name",)
