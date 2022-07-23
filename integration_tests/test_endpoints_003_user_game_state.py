from urllib import response
from integration_tests.helpers import EndpointTestCase


from rest_framework import status
import jwt


from .stub import new_user

target_path = {
    "register" : "/auth/users/"
}
class Test_Story_Login(EndpointTestCase):
    def setUp(self) -> None:

        self.path_register = target_path["register"]
        self.path_login_using_token = "/auth/token/login/"
        self.path_login_using_jwt = "/api/token/"
        self.path_check_access_jwt_valid = "/pokemon/is-my-access-token-valid/"


    def test_registration_and_token_login(self):
        user = new_user()
        assert user.username is not None
        assert user.password is not None

        query_params = {"username": user.username, "password": user.password}

        def register():
            response = self.client.post(self.path_register, query_params)
            response_in_json = response.json()

            assert response.status_code == status.HTTP_201_CREATED

            assert response_in_json["username"] == user.username

        register()

        def login():
            response = self.client.post(self.path_login_using_token, query_params)

            response_in_json = response.json()

            assert response.status_code == status.HTTP_200_OK
            assert response_in_json["auth_token"]

            auth_token = response_in_json["auth_token"]
            user.set_token_auth(auth_token)

        login()

    def test_registration_and_jwt_login(self):

        user = new_user()
        assert user.username is not None
        assert user.password is not None

        query_params = {"username": user.username, "password": user.password}

        def register():
            response = self.client.post(self.path_register, query_params)
            response_in_json = response.json()
            assert response.status_code == status.HTTP_201_CREATED  # [#1-000001]

            assert response_in_json["username"] == user.username

        register()

        def login():  # [#1-000002]
            response = self.client.post(
                self.path_login_using_jwt, query_params, "application/json"
            )

            assert response.status_code == status.HTTP_200_OK
            assert response.headers["Content-Type"] == "application/json"
            response_in_json = response.json()
            assert response_in_json["access"]

            jwt_access_token = response_in_json["access"]
            user.set_token_jwt_access(jwt_access_token)

            jwt_access_token_decoded = jwt.decode(
                jwt_access_token, options={"verify_signature": False}
            )

            assert jwt_access_token_decoded["user_id"]
            assert response_in_json["refresh"]

        login()

        def check_access_token():  # [#1-000003]
            assert user.jwt_access_token is not None

            access_token = user.jwt_access_token

            header_authorization_value = "JWT " + access_token
            headers = {"HTTP_AUTHORIZATION": header_authorization_value}

            response = self.client.post(
                self.path_check_access_jwt_valid,
                content_type="application/json",
                **headers,
            )

            assert response.status_code == status.HTTP_200_OK

        check_access_token()
