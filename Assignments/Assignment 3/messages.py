from datetime import datetime
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Job:
    user: str
    submitted_at: datetime
    status: str
    date_range: Tuple[datetime, datetime]
    assets: List[int]

@dataclass
class Result:
    job_id: str
    timestamp: datetime
    assets_weights: List[Tuple[int, float]]
