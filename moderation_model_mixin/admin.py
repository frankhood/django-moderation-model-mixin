import logging
from urllib.parse import quote

from django.contrib import admin, messages
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http.response import HttpResponseRedirect
from django.utils.encoding import force_str
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class ModerationModelMixinAdmin(admin.ModelAdmin):
    change_form_template = "admin/moderation/moderation_change_form.html"

    actions = ["make_approved", "make_rejected"]
    SHOW_MODERATION = True
    SHOW_MODERATION_FILTER = True
    SHOW_MODERATION_FIELDSETS = True

    fieldsets_moderation = (
        (
            _("Moderation"),
            {"fields": (("display_moderation", "moderation_date"),)},
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if (
            self.SHOW_MODERATION
            and "display_moderation" not in self.list_display
        ):
            self.list_display = list(self.list_display) + [
                "display_moderation"
            ]
        if (
            self.SHOW_MODERATION_FILTER
            and "moderation_state" not in self.list_filter
        ):
            self.list_filter = list(self.list_filter) + ["moderation_state"]
        if (
            (not self.SHOW_MODERATION)
            and self.change_form_template
            == ModerationModelMixinAdmin.change_form_template
        ):
            logger.warning(
                "Pay Attention! You have to set change_form_template=None "
                "if SHOW_MODERATION = False, elsewher set SHOW_MODERATION=True "
                "in this ModelAdmin"
            )

    def get_actions(self, request):
        actions = super().get_actions(request)
        try:
            if not self.SHOW_MODERATION:
                actions.pop("make_approved")
                actions.pop("make_rejected")
        except KeyError:
            pass
        return actions

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj=obj)
        if self.SHOW_MODERATION_FIELDSETS:
            fieldsets = tuple(
                list(fieldsets) + list(self.fieldsets_moderation)
            )
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        return list(readonly_fields) + [
            "display_moderation",
            "moderation_date",
        ]

    @admin.display(
        description=_("Moderation Status"),
        boolean=True,
    )
    def display_moderation(self, obj):
        if obj and obj.id:
            if obj.is_accepted:
                return True
            elif obj.is_rejected:
                return False
        return None

    def response_change(self, request, obj):
        opts = self.model._meta
        preserved_filters = self.get_preserved_filters(request)
        msg_dict = {
            "name": force_str(opts.verbose_name),
            "obj": format_html(
                '<a href="{}">{}</a>', quote(request.path), obj
            ),
        }
        if "_setmoderated" in request.POST:
            obj.set_accepted(commit=True, request=request)
            msg = format_html(
                _(
                    'The {name} "{obj}" was set as "accepted" \
                successfully'
                ),
                **msg_dict,
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts},
                redirect_url,
            )
            return HttpResponseRedirect(redirect_url)
        if "_setrejected" in request.POST:
            obj.set_rejected(commit=True, request=request)
            msg = format_html(
                _(
                    'The {name} "{obj}" was set as "rejected" \
                successfully'
                ),
                **msg_dict,
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts},
                redirect_url,
            )
            return HttpResponseRedirect(redirect_url)
        return super().response_change(request, obj)

    @admin.action(description=_("Accept selected Entries"))
    def make_approved(self, request, queryset):
        updated_objects = 0
        for obj in queryset:
            if obj.is_acceptable():
                obj.set_accepted(commit=True, request=request)
                updated_objects += 1
        message = "{updated_objects} Entry sono state approvate".format(
            **{"updated_objects": updated_objects}
        )
        messages.info(request, message)

    @admin.action(description=_("Reject selected Entries"))
    def make_rejected(self, request, queryset):
        updated_objects = 0
        for obj in queryset:
            if obj.is_rejectable():
                obj.set_rejected(commit=True, request=request)
                updated_objects += 1
        message = "{updated_objects} Entry sono state respinte".format(
            **{"updated_objects": updated_objects}
        )
        messages.info(request, message)
