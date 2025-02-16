from pydantic import BaseModel, constr
from typing import Literal
from datetime import datetime

class TaskCreateDTO(BaseModel):
    title: constr(min_length=1, max_length=100)
    description: constr(min_length=1, max_length=500)
    due_date: datetime
    status: Literal['pending', 'in_progress', 'completed']

class TaskResponseDTO(TaskCreateDTO):
    id: int
    creation_date: datetime

    class Config:
        orm_mode = True
        from_attributes = True
