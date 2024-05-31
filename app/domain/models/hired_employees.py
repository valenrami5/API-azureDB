from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HiredEmployees(BaseModel):

    id: int
    name: Optional[str]
    datetime: Optional[datetime]
    department_id: Optional[int]
    job_id: Optional[int]