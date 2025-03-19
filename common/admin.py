from django.db import models
from unfold.admin import ModelAdmin, StackedInline
from simple_history.admin import SimpleHistoryAdmin
from unfold.widgets import (
    UnfoldAdminSelectWidget,
    UnfoldAdminTextInputWidget,
    UnfoldAdminFileFieldWidget,
)


class BaseInlineAdmin(StackedInline):
    exclude = ["created_at", "updated_at", "created_by", "updated_by"]
    formfield_overrides = {
        models.CharField: {"widget": UnfoldAdminTextInputWidget},
        models.TextField: {"widget": UnfoldAdminTextInputWidget},
        models.ForeignKey: {"widget": UnfoldAdminSelectWidget},
        models.FileField: {"widget": UnfoldAdminFileFieldWidget},
    }

    def has_change_permission(self, request, obj=None):
        return True

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field in self.readonly_fields:
            if field in form.base_fields:
                form.base_fields[field].widget.attrs["disabled"] = True
                form.base_fields[field].required = False
        return form


class BaseModelAdmin(ModelAdmin, SimpleHistoryAdmin):
    readonly_fields = ["created_at", "updated_at", "created_by", "updated_by"]
    exclude = ["created_by", "updated_by"]
    formfield_overrides = {
        models.CharField: {"widget": UnfoldAdminTextInputWidget},
        models.TextField: {"widget": UnfoldAdminTextInputWidget},
        models.ForeignKey: {"widget": UnfoldAdminSelectWidget},
        models.FileField: {"widget": UnfoldAdminFileFieldWidget},
    }

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if fieldsets == [(None, {"fields": list(self.get_fields(request, obj))})]:
            fields = list(self.get_fields(request, obj))
            for field in self.readonly_fields:
                if field in fields:
                    fields.remove(field)
            for field in self.exclude:
                if field in fields:
                    fields.remove(field)

            fieldsets = [
                (None, {"fields": fields}),
                (
                    "Tracking Information",
                    {
                        "fields": self.readonly_fields,
                        # "classes": ("collapse", "collapsed"),
                        # TODO: Unhide tracking information when collapse is fixed
                        "classes": ("hidden",),
                    },
                ),
            ]
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field in self.readonly_fields + self.exclude:
            if field in form.base_fields:
                form.base_fields[field].widget.attrs["disabled"] = True
                form.base_fields[field].required = False
        return form
