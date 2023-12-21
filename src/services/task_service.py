import uuid
import datetime

from typing import Optional, List
from sqlalchemy.orm import Session

from databases.cruds import task_crud
from schemas.task_schema import Task, TaskCreate
from services.common.errors import TaskAlreadyExistsError, TaskNotFoundError


def create_task(db: Session, task:TaskCreate) -> Task:
    exist_task: bool = task_crud.exists_task_by_task_name(db, user_id=task.user_id, task_name=task.task_name) 
    if exist_task:
        raise TaskAlreadyExistsError("このタスク名はすでに存在します。")

    task: Task = Task(
        id=uuid.uuid4(),
        user_id=task.user_id,
        task_name=task.task_name,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )
    
    return task_crud.create_task(db, task)


def get_task_list_by_user_id(db: Session, user_id: str | uuid.UUID) -> List[Task]:
    return task_crud.get_task_list_by_user_id(db, user_id)
