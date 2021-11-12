from unittest.mock import patch

from django.test import TestCase

from tests.test_app.models import ExampleModel


class SignalTest(TestCase):

    # =======================================================================
    # ./manage.py test tests.test_app.tests.test_signals.SignalTest  --settings=tests.settings
    # =======================================================================
    @patch('moderation_model_mixin.signals.set_accepted.send')
    def test_set_accepted_signal(self, mock):

        example = ExampleModel.objects.create()
        example.set_accepted()
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)

    @patch('moderation_model_mixin.signals.set_rejected.send')
    def test_set_rejected_signal(self, mock):

        example = ExampleModel.objects.create()
        example.set_rejected()
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)
