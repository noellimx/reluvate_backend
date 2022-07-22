from urllib import response
from django.test import SimpleTestCase
from pokemon.models import DummyModel
from rest_framework import status

from poke_project.urls import mikecheck_fn

from django.urls import reverse, resolve

from django.test import Client


class EndpointTestCase(SimpleTestCase):
    def setUp(self) -> None:
        self.client = Client()


class TestURLConf_MikeCheck(EndpointTestCase):  # class name should prefix with `Test`
    def test_mikecheck(self):  # function name should prefix with `test_`

        url = reverse("application")
        endpoint = resolve(url)

        self.assertEquals(endpoint.func, mikecheck_fn)

        response = self.client.get("/mikecheck/")

        assert response.status_code == status.HTTP_200_OK


class TestURLConf_App_Pokemon(EndpointTestCase):
    def test_some(self):
        url = reverse("pokemon:hello")
        endpoint = resolve(url)
        print(endpoint.route)
        assert endpoint.route == "pokemon/hello/"

        response = self.client.get("/" + endpoint.route)

        assert response.status_code == status.HTTP_200_OK
        print(response.headers["Content-Type"] == "text/html")
        assert (
            response.content
            == b"Hello world from project [poke_project], app [pokemon]"
        )
