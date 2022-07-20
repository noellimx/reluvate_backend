from django.test import SimpleTestCase
from pokemon.models import DummyModel

from poke_project.urls import mikecheck_fn

from django.urls import reverse, resolve


class TestEndpoints(SimpleTestCase):  # class name should prefix with `Test`
    def test_some_route(self):  # function name should prefix with `test_`

        url = reverse('application')


        endpoint = resolve(url)

        self.assertEquals(endpoint.func, mikecheck_fn)