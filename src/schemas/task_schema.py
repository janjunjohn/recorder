from pydantic import BaseModel


class TaskCreateRequest(BaseModel):
    task_name: str


class TaskNameUpdateRequest(BaseModel):
    task_name: str
