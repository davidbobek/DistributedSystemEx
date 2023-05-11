from pydantic import BaseModel
from enum import Enum


class Role(str, Enum):
    Administrator = "Administrator"
    Secretary = "Secretary"
    Manager = "Manager"

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

    def __str__(self):
        return f"{self.username} {self.password}"


class ChangeRole(BaseModel):
    username: str
    role: Role


class Message(BaseModel):
    pass
    # TODO: add fields
    
class Queue:
    
    def __init__(self, max_size:int, queue_id:str) -> None:
        self.queue = []
        self.queue_id = queue_id
        self.max_size = max_size
    
    def size(self) -> int:
        return len(self.queue)

    def enqueue(self, item:Message) -> bool:
        self.queue.append(item)
        return True
    
    def dequeue(self) -> bool|Message:
        return self.queue.pop(0)
    
