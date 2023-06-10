from pydantic import BaseModel
from enum import Enum


class Status(str, Enum):
    Submitted = "Submitted"
    Processing = "Processing"
    Done = "Done"


class Job(BaseModel):
    id: str
    user: str
    timestamp: str
    status: Status
    date_range: str
    assets: list[int]


class Result(BaseModel):
    job_id: str
    timestamp: str
    assets: float