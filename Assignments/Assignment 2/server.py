# Server that handles requests from the client and sends back the response, but first uses authentication to verify the client using JWT


from fastapi import FastAPI, Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from validation_functions import generate_token, validate_token

from typing import Optional


""" john = User(username="john", password="password")
john.role = Role.Administrator



print(john.role)
"""
from enum import Enum

users = {}


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


app = FastAPI()


# authentication of the user with JWT

users = []
usernames = []
tokens = {}


# create a user with a role and a token
@app.post("/auth/user/")
async def create_user(user_role, username, password, new_role, token):

    tokens[username] = token
    if validate_token(token, "username"):
        if username not in usernames:
            if user_role == "1":
                print("Token is valid \n")
                user = User(username=username, password=password)
                user.role = new_role
                users.append(user)
                usernames.append(username)
                return "User created"
            else:
                return "User is not an administrator"
        else:
            return "User already exists"
    else:
        return "Token is invalid"


# get the user role by username
@app.get("/auth/get_users/")
async def get_user(user_role, username,token):
    if validate_token(token, "username"):
        if username in usernames:
            if user_role == "1":
                print("Token is valid \n")
                # return role of the user by username
                print("users", users)
                return [user.role for user in users if user.username == username]
            else:
                return "User is not an administrator"
        else:
            return "User does not exist"
    else:
        return "Token is invalid"