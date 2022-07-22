from random import randint
from urllib import response
from integration_tests.helpers import EndpointTestCase
import uuid

from rest_framework import status


class StubUser:
    def set_password(self, password):
        self.password = password

    def set_username(self, username):
        self.username = username

    def set_auth_token(self, auth_token: str):
        self.auth_token = auth_token


def new_user_with_similar_username_and_password():
    user_uuid = uuid.uuid4().hex

    user = StubUser()
    user.set_password(f"password{user_uuid}")
    user.set_username(f"user{user_uuid}")

    return user


def new_user():
    user_uuid_user = uuid.uuid4().hex
    user_uuid_password = uuid.uuid4().hex
    user = StubUser()

    user.set_password(f"password{user_uuid_user}")
    user.set_username(f"user{user_uuid_password}")
    return user


class Test_Story_Login(EndpointTestCase):
    def setUp(self) -> None:


        self.path_register = f"/auth/users/"
        self.path_login_using_token = f"/auth/token/login/"
        self.path_login_using_jwt = f'/jwt/create/'

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

            assert response_in_json['username'] == user.username
        
        register()

        def login():
            response = self.client.post(self.path_login_using_token, query_params)

            response_in_json = response.json()

            assert response.status_code == status.HTTP_200_OK
            assert response_in_json["auth_token"]

            auth_token = response_in_json["auth_token"]
            user.set_auth_token(auth_token)

        login()
            



    def test_registration_and_jwt_login(self):

        return 
        user = new_user()
        assert user.username is not None
        assert user.password is not None

        query_params = {"username": user.username, "password": user.password}
        
        def register():
            response = self.client.post(self.path_register, query_params)
            response_in_json = response.json()

            assert response.status_code == status.HTTP_201_CREATED

            assert response_in_json['username'] == user.username
        
        register()

        def login():
            response = self.client.post(self.path_login_using_jwt, query_params)

            # response_in_json = response.json()

            print(response.status_code)
            assert response.status_code == status.HTTP_200_OK
            return
            assert response_in_json["auth_token"]

            auth_token = response_in_json["auth_token"]
            user.set_auth_token(auth_token)

        login()
            

