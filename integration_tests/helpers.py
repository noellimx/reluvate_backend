from django.test import TransactionTestCase

from django.test import Client


class EndpointTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.client = Client()
