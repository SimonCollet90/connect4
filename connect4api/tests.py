from django.test import TestCase


class Connect4APIConfigTest(TestCase):
    def test_app_is_installed(self):
        from django.apps import apps
        self.assertTrue(apps.is_installed('connect4api'))
