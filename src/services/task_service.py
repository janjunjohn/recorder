import uuid
import datetime

from typing import Optional, List
from sqlalchemy.orm import Session

from databases.cruds import task_crud
from services.common.errors import TaskAlreadyExistsError, TaskNotFoundError
from models.user.user_id import UserId
from models.task.task import Task
from models.task.task_id import TaskId


def create_task(db: Session, user_id: UserId, task_name: str) -> Task:
    exist_task: bool = task_crud.exists_task_of_user_by_task_name(db, user_id=user_id, task_name=task_name)
    if exist_task:
        raise TaskAlreadyExistsError("このタスク名はすでに存在します。")

    task: Task = Task(
        id=TaskId(id=uuid.uuid4()),
        user_id=user_id,
        task_name=task_name,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )

    return task_crud.create_task(db, task)


def get_task_list_by_user_id(db: Session, user_id: UserId) -> List[Task]:
    return task_crud.get_task_list_by_user_id(db, user_id)
