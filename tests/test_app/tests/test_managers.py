from django.test import TestCase

from moderation_model_mixin import settings
from moderation_model_mixin.managers import AcceptedModerableEntryManager
from moderation_model_mixin.querysets import ModerableQuerySet
from tests.test_app.models import ExampleModel


class ManagerTest(TestCase):

    # =======================================================================
    # ./manage.py test tests.test_app.tests.test_managers.ManagerTest  --settings=tests.settings
    # =======================================================================

    def test_accepted_items(self):

        example = ExampleModel.objects.create()
        self.assertIn(example, ExampleModel.not_moderated_objects.all())

        example.set_accepted()

        self.assertIn(example, ExampleModel.published_objects.all())
        self.assertIn(example, ExampleModel.accepted_objects.all())
        self.assertIn(example, ExampleModel.not_rejected_objects.all())
        self.assertIn(example, ExampleModel.moderated_objects.all())

        self.assertNotIn(example, ExampleModel.rejected_objects.all())
        self.assertNotIn(example, ExampleModel.not_moderated_objects.all())

        example2 = ExampleModel.objects.create(moderation_state=settings.MODERATION_STATE_ACCEPTED)

        self.assertIn(example2, ExampleModel.published_objects.all())
        self.assertIn(example2, ExampleModel.accepted_objects.all())
        self.assertIn(example2, ExampleModel.not_rejected_objects.all())
        self.assertIn(example2, ExampleModel.moderated_objects.all())

        self.assertNotIn(example2, ExampleModel.rejected_objects.all())
        self.assertNotIn(example2, ExampleModel.not_moderated_objects.all())

    def test_rejected_items(self):
        example = ExampleModel.objects.create()
        self.assertIn(example, ExampleModel.not_moderated_objects.all())
        self.assertIn(example, ExampleModel.not_rejected_objects.all())

        example.set_rejected()

        self.assertIn(example, ExampleModel.moderated_objects.all())
        self.assertIn(example, ExampleModel.rejected_objects.all())

        self.assertNotIn(example, ExampleModel.not_rejected_objects.all())
        self.assertNotIn(example, ExampleModel.accepted_objects.all())
        self.assertNotIn(example, ExampleModel.not_moderated_objects.all())
        self.assertNotIn(example, ExampleModel.published_objects.all())

        example2 = ExampleModel.objects.create(moderation_state=settings.MODERATION_STATE_REJECTED)

        self.assertIn(example2, ExampleModel.moderated_objects.all())
        self.assertIn(example2, ExampleModel.rejected_objects.all())

        self.assertNotIn(example2, ExampleModel.not_rejected_objects.all())
        self.assertNotIn(example2, ExampleModel.accepted_objects.all())
        self.assertNotIn(example2, ExampleModel.published_objects.all())
        self.assertNotIn(example2, ExampleModel.not_moderated_objects.all())
