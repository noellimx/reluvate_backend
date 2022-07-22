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


def new_user_with_similar_username_and_password():
    user_uuid = uuid.uuid4().hex

    user = StubUser()
    user.set_password(f"password{user_uuid}")
    user.set_username(f"user{user_uuid}")

    return user


def new_user_1():
    user_uuid_user = uuid.uuid4().hex
    user_uuid_password = uuid.uuid4().hex
    user = StubUser()

    user.set_password(f"password{user_uuid_user}")
    user.set_username(f"user{user_uuid_password}")
    return user


class Test_Story_Login(EndpointTestCase):
    def setUp(self) -> None:
        self.user1 = new_user_1()
        assert self.user1.username is not None
        assert self.user1.password is not None

        self.path_login = f"/auth/users/"

    def test_empty_username_and_password_login(self):
        response = self.client.get("/auth/users/me/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_register_with_too_similar_credentials(self):

        user = new_user_with_similar_username_and_password()
        query_params = {"username": user.username, "password": user.password}
        response = self.client.post(self.path_login, query_params)
        response_in_json = response.json()

        print(response_in_json)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_in_json["password"] == [
            "The password is too similar to the username."
        ]

    def test_registration_and_token_login(self):

        return
        query_params = {
            "username": self.user1.username,
            "password": self.user1.password,
        }
        query_string = f"username={self.user1.username}&password={self.user1.password}"

        path = f"/auth/users/"
        response = self.client.post(path, query_params)
        print(response.status_code)
        print(response.headers)

        print(path)
        assert response.status_code == status.HTTP_200_OK

        # response = self.client.post("/auth/token/login/", query_string)
        # print(response.status_code)
        # print(response.headers)

        # assert(response.status_code == status.HTTP_200_OK)
