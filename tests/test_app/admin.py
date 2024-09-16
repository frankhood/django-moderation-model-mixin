from django.contrib import admin

from moderation_model_mixin.admin import ModerationModelMixinAdmin
from tests.test_app.models import ExampleModel


@admin.register(ExampleModel)
class ExampleModelAdmin(ModerationModelMixinAdmin, admin.ModelAdmin):
    pass
