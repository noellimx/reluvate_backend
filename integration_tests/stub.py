import uuid


class StubUser:
    def set_password(self, password):
        self.password = password

    def set_username(self, username):
        self.username = username

    def set_token_auth(self, auth_token: str):
        self.auth_token = auth_token

    def set_token_jwt_access(self, jwt_access_token: str):
        self.jwt_access_token = jwt_access_token


def new_user():
    user_uuid_user = uuid.uuid4().hex
    user_uuid_password = uuid.uuid4().hex[:6]
    user = StubUser()

    user.set_password(f"password{user_uuid_user}")
    user.set_username(f"user{user_uuid_password}")
    return user
