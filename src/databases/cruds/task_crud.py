from typing import List


from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from databases.models.task import Task as TaskTable
from databases.models.user import User as UserTable
from models.user.user_id import UserId
from models.task.task import Task
from models.task.task_id import TaskId
from services.common.errors import TaskNotFoundError


def exists_task_of_user_by_task_name(db: Session, user_id: UserId, task_name: str) -> bool:
    query = db.query(TaskTable).filter(TaskTable.user_id == user_id.id, TaskTable.task_name == task_name)
    return db.query(query.exists()).scalar()


def exists_task_by_id(db: Session, task_id: TaskId) -> bool:
    query = db.query(TaskTable).filter(TaskTable.id == task_id.id)
    return db.query(query.exists()).scalar()


def create_task(db: Session, task: Task) -> Task:
    db_task: TaskTable = TaskTable(id=task.id.id, user_id=task.user_id.id, task_name=task.task_name)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return Task(id=TaskId(id=db_task.id), user_id=UserId(id=db_task.user_id), task_name=db_task.task_name,
                created_at=db_task.created_at, updated_at=db_task.updated_at)


def update_task_name(db: Session, task: Task) -> Task:
    db_task: TaskTable = db.query(TaskTable).filter(TaskTable.task_id == task.id.id).one()
    db_task.task_name = task.task_name
    db.commit()
    db.refresh(db_task)
    return Task(id=TaskId(id=db_task.id), user_id=UserId(id=db_task.user_id), task_name=db_task.task_name,
                created_at=db_task.created_at, updated_at=db_task.updated_at)


def delete_task(db: Session, task_id: TaskId) -> None:
    db_task: TaskTable = db.query(TaskTable).filter(TaskTable.id == task_id.id).one()
    db.delete(db_task)
    db.commit()


def get_task_by_id(db: Session, user_id: UserId, task_id: TaskId) -> Task:
    try:
        db_task: TaskTable = db.query(TaskTable).filter(UserTable.id == user_id.id, TaskTable.id == task_id.id).one()
        return Task(id=TaskId(id=db_task.id), user_id=UserId(id=db_task.user_id), task_name=db_task.task_name,
                    created_at=db_task.created_at, updated_at=db_task.updated_at)
    except NoResultFound:
        raise TaskNotFoundError("タスクが見つかりませんでした")


def get_task_list_by_user_id(db: Session, user_id: UserId) -> List[Task]:
    db_task_list = db.query(TaskTable).filter(TaskTable.user_id == user_id.id).all()
    task_list = []
    for db_task in db_task_list:
        task = Task(
            id=TaskId(id=db_task.id), user_id=UserId(id=db_task.user_id), task_name=db_task.task_name,
            created_at=db_task.created_at, updated_at=db_task.updated_at
        )
        task_list.append(task)
    return task_list
