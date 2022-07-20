from django.test import SimpleTestCase
from pokemon.models import DummyModel
from rest_framework import status

from poke_project.urls import mikecheck_fn

from django.urls import reverse, resolve

from django.test import Client


class TestEndpoints(SimpleTestCase):  # class name should prefix with `Test`

    def setUp(self) -> None:
        self.client = Client()

    def test_some_route(self):  # function name should prefix with `test_`

        url = reverse('application')
        endpoint = resolve(url)

        self.assertEquals(endpoint.func, mikecheck_fn)

        response = self.client.get("/mikecheck/")

        assert(response.status_code == status.HTTP_200_OK)
