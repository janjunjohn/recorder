import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

from services.common.errors import ValidationError
from models.user.user_id import UserId
from models.task.task_id import TaskId


class Task(BaseModel):
    id: TaskId
    user_id: UserId
    task_name: str
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    @field_validator('task_name')
    def task_name_is_valid(cls, task_name):
        if len(task_name) < 1:
            raise ValueError('タスク名は1文字以上にしてください。')
        if len(task_name) > 15:
            raise ValueError('タスク名は15文字以下にしてください。')
        return task_name
