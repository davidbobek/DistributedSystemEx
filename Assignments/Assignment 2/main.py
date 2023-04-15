from fastapi import FastAPI, Depends, HTTPException
from schemas import User, Role, Login, Token, DeleteRequest
from auth import AuthHandler

app = FastAPI()
authHandler = AuthHandler()
global_token = None
db = [
    User(username="admin", password=authHandler.get_password_hash("admin"), role=Role.Administrator),
    User(username='secretary', password=authHandler.get_password_hash("secretary"), role=Role.Secretary),
    User(username='manager', password=authHandler.get_password_hash("manager"), role=Role.Manager)
]


# this is a test
@app.get("/auth/users/")
async def get_users():
    return db


@app.post("/auth/login/")
def login(auth_details: Login):
    global global_token
    user = None  # user is set to None
    for x in db:  # check the existance of the user in the database
        if x.username == auth_details.username:
            user = x
            break
    if user is None: # if the user doesn't exist, raise an error
        raise HTTPException(status_code=401, detail='Invalid username')
    if not authHandler.verify_password(auth_details.password, user.password):  # if the password is incorrect, raise an error
        raise HTTPException(status_code=401, detail='Invalid password')
    token = authHandler.encode_token(user.username)  # if the user exists and the password is correct, generate a token
    global_token = token  # set the global token to the generated token
    return {'token': token }  # return the token
    
    
@app.post("/auth/manage/")
async def create_user(token:str, user: User) -> int:  
    request = authHandler.decode_token(token)  # decode the token and get the dict with data
    for u in db:  # check the existance of the user in the database
        if request == u.username:  # if the user exists
            if u.role == Role.Administrator:  # check the role
                if any(x.username == user.username for x in db):  # check the existance of the username in the database
                    raise HTTPException(status_code=409, detail="Username taken")  # if the username exists, raise an error
                db.append(user)  # if the username doesn't exist, add the user to the database
                return 200  # return 200 if the user was added
            else:
                raise HTTPException(status_code=403, detail="Not admin")  # if the user is not admin, raise an error
    return 404  # if the user doesn't exist, return 404
 
 
@app.delete("/auth/manage/")
async def delete_user(delete: DeleteRequest) -> int:
    request = authHandler.decode_token(delete.token)
    for user in db:
        if request == user.username:
            if user.role == Role.Administrator:
                for user in db:
                    if user.username == delete.username:
                        db.remove(user)
                        return 200
            else:
                raise HTTPException(status_code=403, detail="Not admin")
    return 404


@app.post("/auth/logout/")
async def logout(token:Token):  # logout
    global global_token
    if global_token is None:  # if the global token is None, raise an error
        raise HTTPException(status_code=401, detail="Not logged in")
    request = authHandler.decode_token(token.token)  # decode the token and get the dict with data
    for user in db:  # check the existance of the user in the database
        if request == user.username:  # if the user exists
            global_token = None  # set the global token to None
            return 200


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)