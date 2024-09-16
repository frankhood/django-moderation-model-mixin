from django.test import TestCase

from moderation_model_mixin import settings
from moderation_model_mixin.querysets import ModerableQuerySet
from tests.test_app.models import ExampleModel


class QuerySetTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.moderable_queryset = ModerableQuerySet(ExampleModel)

    # =======================================================================
    # ./manage.py test tests.test_app.tests.test_querysets.QuerySetTest  --settings=tests.settings
    # =======================================================================

    def test_accepted_items(self):

        example = ExampleModel.objects.create()
        self.assertIn(example, self.moderable_queryset.not_moderated())
        self.assertIn(example, self.moderable_queryset.not_rejected())

        example.set_accepted()

        self.assertIn(example, self.moderable_queryset.accepted())
        self.assertIn(example, self.moderable_queryset.moderated())
        self.assertIn(example, self.moderable_queryset.not_rejected())

        self.assertNotIn(example, self.moderable_queryset.rejected())
        self.assertNotIn(example, self.moderable_queryset.not_moderated())

        example2 = ExampleModel.objects.create(
            moderation_state=settings.MODERATION_STATE_ACCEPTED
        )

        self.assertIn(example2, self.moderable_queryset.accepted())
        self.assertIn(example2, self.moderable_queryset.moderated())
        self.assertIn(example2, self.moderable_queryset.not_rejected())

        self.assertNotIn(example2, self.moderable_queryset.rejected())
        self.assertNotIn(example2, self.moderable_queryset.not_moderated())

    def test_rejected_items(self):
        example = ExampleModel.objects.create()
        self.assertIn(example, self.moderable_queryset.not_moderated())
        self.assertIn(example, self.moderable_queryset.not_rejected())

        example.set_rejected()

        self.assertIn(example, self.moderable_queryset.moderated())
        self.assertIn(example, self.moderable_queryset.rejected())

        self.assertNotIn(example, self.moderable_queryset.not_rejected())
        self.assertNotIn(example, self.moderable_queryset.accepted())
        self.assertNotIn(example, self.moderable_queryset.not_moderated())

        example2 = ExampleModel.objects.create(
            moderation_state=settings.MODERATION_STATE_REJECTED
        )

        self.assertIn(example2, self.moderable_queryset.moderated())
        self.assertIn(example2, self.moderable_queryset.rejected())

        self.assertNotIn(example2, self.moderable_queryset.not_rejected())
        self.assertNotIn(example2, self.moderable_queryset.accepted())
        self.assertNotIn(example2, self.moderable_queryset.not_moderated())
