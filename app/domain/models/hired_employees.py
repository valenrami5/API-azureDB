from pydantic import BaseModel
from datetime import datetime

class HiredEmployees(BaseModel):

    id: str
    name: str
    datetime: datetime
    department_id: int
    job_id: int