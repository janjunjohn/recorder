import uuid
import datetime

from pydantic import BaseModel, field_validator
from typing import Optional


class TaskBase(BaseModel):
    user_id: str | uuid.UUID
    task_name: str

    @field_validator('task_name')
    def task_name_is_valid(cls, task_name):
        if len(task_name) < 1:
            raise ValueError('タスク名は1文字以上にしてください。')
        if len(task_name) > 15:
            raise ValueError('タスク名は15文字以下にしてください。')
        return task_name
    

class TaskCreate(TaskBase):
    pass
    

class Task(TaskBase):
    id: str | uuid.UUID
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    
    class Config:
        orm_mode = True
