from django.test import TestCase

from moderation_model_mixin import settings
from moderation_model_mixin.querysets import ModerableQuerySet
from tests.test_app.models import ExampleModel


class ModelTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

    # =======================================================================
    # ./manage.py test tests.test_app.tests.test_models.ModelTest  --settings=tests.settings
    # =======================================================================
    def test_unit(self):
        example = ExampleModel.objects.create()
        self.assertEqual(example.moderation_state, settings.MODERATION_STATE_QUEUED)
        self.assertTrue(example.is_rejectable())
        self.assertTrue(example.is_acceptable())
        self.assertTrue(example.is_actual)

        self.assertFalse(example.is_moderated)
        self.assertFalse(example.is_rejected)
        self.assertFalse(example.is_accepted)
        self.assertFalse(example.is_sharable)

        example.set_accepted()
        self.assertEqual(example.moderation_state, settings.MODERATION_STATE_ACCEPTED)
        self.assertTrue(example.is_rejectable())
        self.assertTrue(example.is_actual)
        self.assertTrue(example.is_moderated)
        self.assertTrue(example.is_accepted)
        self.assertTrue(example.is_sharable)

        self.assertFalse(example.is_acceptable())
        self.assertFalse(example.is_rejected)

        example.set_rejected()
        self.assertEqual(example.moderation_state, settings.MODERATION_STATE_REJECTED)
        self.assertTrue(example.is_moderated)
        self.assertTrue(example.is_rejected)

        self.assertFalse(example.is_rejectable())
        self.assertFalse(example.is_actual)
        self.assertFalse(example.is_accepted)
        self.assertFalse(example.is_sharable)
        self.assertFalse(example.is_acceptable())

    def test_previous_next(self):
        for i in range(0, 3):
            ExampleModel.objects.create()

        qs = ExampleModel.not_moderated_objects.all()
        last = qs.last()
        last.set_accepted()
        first = qs.first()
        first.set_accepted()
        middle = qs.first()
        middle.set_accepted()

        previous_of_first = first.get_previous()
        self.assertEqual(last, previous_of_first)

        next_of_first = first.get_next()
        self.assertEqual(middle, next_of_first)

