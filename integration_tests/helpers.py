from django.test import SimpleTestCase

from django.test import Client


class EndpointTestCase(SimpleTestCase):
    def setUp(self) -> None:
        self.client = Client()
