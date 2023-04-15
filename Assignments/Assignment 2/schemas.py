from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    Administrator = "1"
    Secretary = "2"
    Manager = "3"
    
    def __str__(self):
        return f"{self.value}"
    
class User(BaseModel):
    username: str
    password: str
    role: Role
    
    def __str__(self):
        return f"{self.username} {self.password} {self.role}"

class Login(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    token: str
    
class DeleteRequest(BaseModel):
    token: str
    username: str