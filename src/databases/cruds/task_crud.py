import uuid
from typing import List


from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import DataError

from databases.models.task import Task as TaskTable
from schemas.task_schema import Task
from services.common.errors import TaskNotFoundError, InvalidUUIDError


def exists_task_of_user_by_task_name(db: Session, task_name: str, user_id: str | uuid.UUID) -> bool:
    query = db.query(TaskTable).filter(TaskTable.user_id == user_id, TaskTable.task_name == task_name)
    return db.query(query.exists()).scalar()


def create_task(db:Session, task: Task) -> Task:
    db_task = TaskTable(id=task.id, user_id=task.user_id, task_name=task.task_name,
                        created_at=task.created_at, updated_at=task.updated_at)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return Task(id=db_task.id, user_id=db_task.user_id, task_name=db_task.task_name,
                created_at=db_task.created_at, updated_at=db_task.updated_at)


def get_task_list_by_user_id(db: Session, user_id: str | uuid.UUID) -> List[Task]:
    try:
        db_task_list = db.query(TaskTable).filter(TaskTable.user_id == user_id).all()
    except DataError:
        raise InvalidUUIDError("不正なidです")
    task_list = [] 
    for db_task in db_task_list:
        task = Task(
            user_id=db_task.user_id, task_name=db_task.task_name, id=db_task.id,
            created_at=db_task.created_at, updated_at=db_task.updated_at
        )
        task_list.append(task)
    return task_list
