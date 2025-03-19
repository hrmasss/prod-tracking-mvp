from django import forms
from users.models import Department, Role, User
from django.contrib.auth.models import Permission
from unfold.forms import (
    UserChangeForm as BaseUserChangeForm,
    UserCreationForm as BaseUserCreationForm,
)


class DepartmentAdminForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields.get("permissions"):
            self.fields["permissions"].queryset = Permission.objects.exclude(
                codename__contains="historical"
            )


class RoleAdminForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields.get("permissions"):
            self.fields["permissions"].queryset = Permission.objects.exclude(
                codename__contains="historical"
            )


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields.get("user_permissions"):
            self.fields["user_permissions"].queryset = Permission.objects.exclude(
                codename__contains="historical"
            )


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = "__all__"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user
