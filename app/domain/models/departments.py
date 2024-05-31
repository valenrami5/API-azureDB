from pydantic import BaseModel

class Departments(BaseModel):

    id: int
    department: str