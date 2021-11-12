from django.contrib import admin
from moderation_model_mixin.admin import ModerationModelMixinAdmin
from tests.test_app.models import ExampleModel


class ExampleModelAdmin(ModerationModelMixinAdmin, admin.ModelAdmin):
    ...


admin.site.register(ExampleModel, ExampleModelAdmin)
