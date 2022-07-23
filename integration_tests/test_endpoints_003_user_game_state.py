from urllib import response

from django import http
from integration_tests.helpers import EndpointTestCase


from rest_framework import status
import jwt


from .stub import new_user

from .targets import target_path


class Test_Story_PlayGuessingGame_WithoutRewards(EndpointTestCase):
    def setUp(self) -> None:

        self.path_register = target_path["register"]
        self.path_login_using_jwt = target_path["login_using_jwt"]
        self.path_how_many_tries_already = target_path["how_many_tries_already"]

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

    def test_initial_state_user_tried_0_times(self):
        header_authorization_value = "JWT " + self.user.jwt_access_token
        headers = {"HTTP_AUTHORIZATION": header_authorization_value}

        response = self.client.get(self.path_how_many_tries_already, **headers)

        assert response.status_code == status.HTTP_200_OK
