from integration_tests.helpers import EndpointTestCase
import uuid

from rest_framework import status
import jwt


from .stub import StubUser, new_user
from .targets import target_path


def new_user_with_similar_username_and_password():
    user_uuid = uuid.uuid4().hex

    user = StubUser()
    user.set_password(f"password{user_uuid}")
    user.set_username(f"user{user_uuid}")

    return user


class Test_Story_Login(EndpointTestCase):
    def setUp(self) -> None:
        self.path_register = target_path["register"]
        self.path_login_using_token = target_path["login_using_token"]
        self.path_login_using_jwt = target_path["login_using_jwt"]
        self.path_check_access_jwt_valid = target_path["check_access_jwt_valid"]

    def test_empty_username_and_password_login(self):
        response = self.client.get("/auth/users/me/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_register_with_too_similar_credentials(self):

        user = new_user_with_similar_username_and_password()
        query_params = {"username": user.username, "password": user.password}
        response = self.client.post(self.path_register, query_params)
        response_in_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_in_json["password"] == [
            "The password is too similar to the username."
        ]

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
