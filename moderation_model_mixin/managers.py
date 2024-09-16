import logging

from django.db import models

from moderation_model_mixin.querysets import ModerableQuerySet

logger = logging.getLogger(__name__)


class ModerableEntryManager(models.Manager):
    def get_queryset(self):
        return ModerableQuerySet(self.model, using=self._db)


class AcceptedModerableEntryManager(ModerableEntryManager):
    def get_queryset(self):
        return super().get_queryset().accepted()


class ModeratedModerableEntryManager(ModerableEntryManager):
    def get_queryset(self):
        return super().get_queryset().moderated()


class NotModeratedModerableEntryManager(ModerableEntryManager):
    def get_queryset(self):
        return super().get_queryset().not_moderated()


class RejectedModerableEntryManager(ModerableEntryManager):
    def get_queryset(self):
        return super().get_queryset().rejected()


class NotRejectedModerableEntryManager(ModerableEntryManager):
    def get_queryset(self):
        return super().get_queryset().not_rejected()
