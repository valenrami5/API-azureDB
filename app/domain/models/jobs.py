from pydantic import BaseModel
from datetime import datetime

class Jobs(BaseModel):
    id: int
    job: str