import uuid

from typing import List
from sqlalchemy.orm import Session

from databases.cruds import task_crud
from services.common.errors import TaskAlreadyExistsError, TaskNotFoundError
from models.user.user_id import UserId
from models.task.task import Task
from models.task.task_id import TaskId
from schemas.task_schema import TaskCreateRequest, TaskNameUpdateRequest


def get_task_by_id(db: Session, user_id: UserId, task_id: TaskId) -> Task:
    return task_crud.get_task_by_id(db, user_id, task_id)


def create_task(db: Session, user_id: UserId, task_create: TaskCreateRequest) -> Task:
    exist_task_name: bool = task_crud.exists_task_of_user_by_task_name(
        db, user_id=user_id, task_name=task_create.task_name
    )
    if exist_task_name:
        raise TaskAlreadyExistsError("このタスク名はすでに存在します。")

    task: Task = Task(
        id=TaskId(id=uuid.uuid4()),
        user_id=user_id,
        task_name=task_create.task_name,
    )

    return task_crud.create_task(db, task)


def update_task_name(db: Session, user_id: UserId, task_id: TaskId, task_name_update: TaskNameUpdateRequest) -> Task:
    exist_task_name: bool = task_crud.exists_task_of_user_by_task_name(
        db, user_id=user_id, task_name=task_name_update.task_name
    )
    if exist_task_name:
        raise TaskAlreadyExistsError("このタスク名はすでに存在します。")
    task: Task = get_task_by_id(db, user_id, task_id)
    updated_task: Task = Task(
        id=TaskId(id=task_id.id),
        user_id=UserId(task.user_id.id),
        task_name=task_name_update.task_name
    )
    return task_crud.update_task_name(db, updated_task)


def delete_task(db: Session, task_id: TaskId) -> None:
    exists_task: bool = task_crud.exists_task_by_task_id(db, task_id)
    if not exists_task:
        raise TaskNotFoundError("タスクが見つかりませんでした")
    return task_crud.delete_task(task_id)


def get_task_list_by_user_id(db: Session, user_id: UserId) -> List[Task]:
    return task_crud.get_task_list_by_user_id(db, user_id)
