import requests


from enum import Enum

from validation_functions import generate_token, validate_token


class Role(Enum):
    Administrator = 1

    Secretary = 2

    Manager = 3

    def __str__(self):
        return f"{self.value}"


class User:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.role = None
        self.token = None


def admin_creation():
    john = User(username="john", password="password")
    john.role = Role.Administrator
    token = generate_token("username")
    john.token = token

    return john


# create a user with a role and a token on the server
def create_user(user):
    url = "http://localhost:8000/auth/user/"
    params = {
        "user_role": user.role,
        "username": "john",
        "password": "password123",
        "new_role": "1",
        "token": user.token,
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        print("Creating user on server")
        data = response.json()
        print(data)

# get a user from the server with a username
def get_user(user, username):
    url = "http://localhost:8000/auth/get_users"
    params = {
        "user_role": user.role,
        "username": username,
        "token": user.token,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Getting users from server")
        data = response.json()
        print(data)


if __name__ == "__main__":
    user = admin_creation()
    create_user(user)
    get_user(user,"john")

    #When I run this code I get the following response: User does not exist
    #get_user(user,"john2")
