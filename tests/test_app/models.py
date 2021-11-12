from django.db import models

from moderation_model_mixin.models import ModerationModelMixin


class ExampleModel(ModerationModelMixin, models.Model):
    ...
