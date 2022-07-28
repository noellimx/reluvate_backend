from integration_tests.helpers import EndpointTestCase


from rest_framework import status
import jwt

from pokemon.views import guess


from .stub import new_user

from .targets import target_path
from .helpers import ORACLE_TARGET
import json


class Test_Story_PlayGuessingGame_Pokemon(EndpointTestCase):
    def setUp(self) -> None:

        print("[Test_Story_PlayGuessingGame_Pokemon] setUp")

        self.path_register = target_path["register"]
        self.path_login_using_jwt = target_path["login_using_jwt"]
        self.path_how_many_tries_already = target_path["how_many_tries_already"]
        self.path_guess = target_path["guess"]
        self.path_unowned_pokedex = target_path["unowned_pokedex"]
        self.path_owned_pokemon = target_path["owned_pokemon"]

        self.user = new_user()
        assert self.user.username is not None
        assert self.user.password is not None

        query_params = {"username": self.user.username, "password": self.user.password}

        def register():
            response = self.client.post(self.path_register, query_params)
            response_in_json = response.json()

            assert response.status_code == status.HTTP_201_CREATED
            assert response_in_json["username"] == self.user.username

        register()

        def login_jwt():
            response = self.client.post(
                self.path_login_using_jwt, query_params, "application/json"
            )

            assert response.status_code == status.HTTP_200_OK
            assert response.headers["Content-Type"] == "application/json"
            response_in_json = response.json()
            assert response_in_json["access"]

            jwt_access_token = response_in_json["access"]

            jwt_access_token_decoded = jwt.decode(
                jwt_access_token, options={"verify_signature": False}
            )

            assert jwt_access_token_decoded["user_id"]
            assert response_in_json["refresh"]

            self.user.set_token_jwt_access(jwt_access_token)

        login_jwt()

    def test_pokemon_portfolio(self):

        header_authorization_value = "JWT " + self.user.jwt_access_token
        headers = {"HTTP_AUTHORIZATION": header_authorization_value}

        def owned_pokemon_should_be_none():
            response = self.client.get(
                self.path_owned_pokemon,
                {},
                **headers,
            )
            assert response.status_code == status.HTTP_200_OK

            response_in_json = response.json()

            pokemons = json.loads(response_in_json["pokemons"])

            assert len(pokemons) == 0

        owned_pokemon_should_be_none()

        def unowned_pokedex_should_be_all_pokemons():

            response = self.client.get(
                self.path_unowned_pokedex,
                {},
                **headers,
            )

            assert response.status_code == status.HTTP_200_OK

            response_in_json = response.json()

            pokemons = response_in_json["pokedex"]

            assert len(pokemons) == 16

        unowned_pokedex_should_be_all_pokemons()

        def guess_correct():
            correct_guess = ORACLE_TARGET
            d = {"guess": correct_guess}

            response = self.client.post(
                self.path_guess,
                data=json.dumps(d),
                content_type="application/json",
                **headers,
            )

        guess_correct()

        def owned_pokemon_should_be_one():
            print("[owned_pokemon_should_be_one]")

            response = self.client.get(
                self.path_owned_pokemon,
                {},
                **headers,
            )
            assert response.status_code == status.HTTP_200_OK
            response_in_json = response.json()
            pokemons = json.loads(response_in_json["pokemons"])
            assert len(pokemons) == 1

            first_pokemon = pokemons[0]
            assert first_pokemon["id"]
            assert first_pokemon["pokedex"]
            assert first_pokemon["pokedex"]["pokename"]
            assert first_pokemon["trainer"]["username"] == self.user.username

        owned_pokemon_should_be_one()

        def unowned_pokedex_should_be_all_pokemons_except_prize_rewarded():

            response = self.client.get(
                self.path_unowned_pokedex,
                {},
                **headers,
            )

            assert response.status_code == status.HTTP_200_OK

            response_in_json = response.json()

            pokemons = response_in_json["pokedex"]

            assert len(pokemons) == 15

        unowned_pokedex_should_be_all_pokemons_except_prize_rewarded()
