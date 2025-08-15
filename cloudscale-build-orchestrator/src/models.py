from pydantic import BaseModel, Field
from typing import List, Optional
import time

class Step(BaseModel):
    cmd: str
    cache_key: Optional[str] = None
    timeout_sec: int = 120
    retries: int = 1

class BuildRequest(BaseModel):
    name: str = Field(..., min_length=1)
    steps: List[Step]

class BuildStatus(BaseModel):
    run_id: str
    name: str
    status: str
    started_at: float
    finished_at: Optional[float] = None
    logs: List[str] = []
