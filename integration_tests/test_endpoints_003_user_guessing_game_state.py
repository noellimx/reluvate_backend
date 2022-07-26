from integration_tests.helpers import EndpointTestCase


from rest_framework import status
import jwt

from pokemon.views import guess


from .stub import new_user

from .targets import target_path
from .helpers import ORACLE_TARGET
import json


class Test_Story_PlayGuessingGame_WithoutRewards(EndpointTestCase):
    def setUp(self) -> None:

        print("[Test_Story_PlayGuessingGame_WithoutRewards] setUp")

        self.path_register = target_path["register"]
        self.path_login_using_jwt = target_path["login_using_jwt"]
        self.path_how_many_tries_already = target_path["how_many_tries_already"]
        self.path_guess = target_path["guess"]

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

    def test_tried_state_no_correct_guess(self):
        print("[test_tried_state_no_correct_guess]")
        header_authorization_value = "JWT " + self.user.jwt_access_token
        headers = {"HTTP_AUTHORIZATION": header_authorization_value}
        initial_state = 0

        def initial_state_user_tried_0_times():

            response = self.client.get(self.path_how_many_tries_already, {}, **headers)
            assert response.status_code == status.HTTP_200_OK
            assert response.headers["Content-Type"] == "application/json"

            response_in_json = response.json()
            assert response_in_json["tried"] == initial_state
            assert response_in_json["prize"]

            prize = json.loads(response_in_json["prize"])

            assert prize["id"]
            assert prize["pokedex"]
            assert prize["pokedex"]["pokename"]

        initial_state_user_tried_0_times()

        def first_valid_incorrect_guess():
            print("[first_valid_incorrect_guess]")
            end_state = 1

            guess = 0

            d = {"guess": guess}

            response = self.client.post(
                self.path_guess,
                data=json.dumps(d),
                content_type="application/json",
                **headers
            )

            assert response.json()["tried"] == end_state
            assert response.status_code == status.HTTP_200_OK

        first_valid_incorrect_guess()

        def second_valid_incorrect_guess():
            print("[second_valid_incorrect_guess]")
            end_state = 2

            guess = 5555

            d = {"guess": guess}

            response = self.client.post(
                self.path_guess,
                data=json.dumps(d),
                content_type="application/json",
                **headers
            )

            assert response.json()["tried"] == end_state
            assert response.status_code == status.HTTP_200_OK

        second_valid_incorrect_guess()

        def invalid_guess_should_not_change_tried_state():
            print("[invalid_guess_should_not_change_tried_state]")
            response = self.client.get(self.path_how_many_tries_already, {}, **headers)
            tried = response.json()["tried"]
            end_state = tried

            guess_not_a_number = ""
            d = {"guess": guess_not_a_number}

            response = self.client.post(
                self.path_guess,
                data=json.dumps(d),
                content_type="application/json",
                **headers
            )

            assert response.json()["tried"] == end_state
            assert response.status_code == status.HTTP_200_OK

        invalid_guess_should_not_change_tried_state()

        def third_valid_incorrect_guess_should_reset_tried_to_initial():
            print("[third_valid_incorrect_guess_should_reset_tried_to_initial]")
            guess = 0

            d = {"guess": guess}

            response = self.client.post(
                self.path_guess,
                data=json.dumps(d),
                content_type="application/json",
                **headers
            )

            assert response.json()["tried"] == initial_state
            assert response.status_code == status.HTTP_200_OK

        third_valid_incorrect_guess_should_reset_tried_to_initial()

    def test_tried_state_correct_guess(self):
        print("[test_tried_state_correct_guess]")

        initial_state = 0
        header_authorization_value = "JWT " + self.user.jwt_access_token
        headers = {"HTTP_AUTHORIZATION": header_authorization_value}

        def correct_guess_should_reset_tried_to_initial():
            guess = ORACLE_TARGET
            d = {"guess": guess}

            response = self.client.post(
                self.path_guess,
                data=json.dumps(d),
                content_type="application/json",
                **headers
            )

            assert response.json()["tried"] == initial_state
            assert response.status_code == status.HTTP_200_OK

        correct_guess_should_reset_tried_to_initial()

        def some_wrong_guess_then_correct_should_reset_tried_to_initial():
            wrong_guess = 2356236
            d = {"guess": wrong_guess}

            self.client.post(
                self.path_guess,
                data=json.dumps(d),
                content_type="application/json",
                **headers
            )
            correct_guess = ORACLE_TARGET
            d = {"guess": correct_guess}

            response = self.client.post(
                self.path_guess,
                data=json.dumps(d),
                content_type="application/json",
                **headers
            )
            assert response.status_code == status.HTTP_200_OK

            response_in_json = response.json()
            assert response_in_json["tried"] == initial_state
            assert response_in_json["reply"] == "hit"

        some_wrong_guess_then_correct_should_reset_tried_to_initial()

    def test_correct_guess_should_transfer_prize_ownership(self):
        print("[test_correct_guess_should_transfer_prize_ownership]")
        header_authorization_value = "JWT " + self.user.jwt_access_token
        headers = {"HTTP_AUTHORIZATION": header_authorization_value}

        def get_prize_to_be_won():
            response = self.client.get(self.path_how_many_tries_already, {}, **headers)
            response_in_json = response.json()
            prize = json.loads(response_in_json["prize"])

            assert prize["pokedex"]["pokename"]
            assert prize["id"]
            self.expected_prize = {
                "id": prize["id"],
                "pokename": prize["pokedex"]["pokename"],
            }

        get_prize_to_be_won()

        def guess_correct_should_win_prize_and_refresh_prize():

            correct_guess = ORACLE_TARGET
            d = {"guess": correct_guess}

            response = self.client.post(
                self.path_guess,
                data=json.dumps(d),
                content_type="application/json",
                **headers
            )
            response_in_json = response.json()
            assert response_in_json["reply"] == "hit"
            assert response_in_json["prize_rewarded"]
            prize_rewarded = json.loads(response_in_json["prize_rewarded"])
            assert prize_rewarded["trainer"]
            assert prize_rewarded["trainer"]["username"] == self.user.username
            assert self.expected_prize["id"] == prize_rewarded["id"]
            assert (
                self.expected_prize["pokename"] == prize_rewarded["pokedex"]["pokename"]
            )

            assert response_in_json["prize_next"]
            print("---aa-")
            print(response_in_json["prize_next"])
            print(type(response_in_json["prize_next"]))
            prize_next = json.loads(response_in_json["prize_next"])
            assert prize_next["id"] != self.expected_prize["id"]

        guess_correct_should_win_prize_and_refresh_prize()
