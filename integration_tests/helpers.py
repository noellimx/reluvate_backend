from django.test import TransactionTestCase

from django.test import Client


class ApplicationStartupTestCase(TransactionTestCase):
    serialized_rollback: bool = True


class EndpointTestCase(ApplicationStartupTestCase):
    def setUp(self) -> None:
        self.client = Client()
