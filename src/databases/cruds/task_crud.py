from typing import List


from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from databases.models.task import Task as TaskTable
from models.user.user_id import UserId
from models.task.task import Task
from models.task.task_id import TaskId


def exists_task_of_user_by_task_name(db: Session, user_id: UserId, task_name: str) -> bool:
    query = db.query(TaskTable).filter(TaskTable.user_id == user_id.id, TaskTable.task_name == task_name)
    return db.query(query.exists()).scalar()


def create_task(db: Session, task: Task) -> Task:
    db_task = TaskTable(id=task.id.id, user_id=task.user_id.id, task_name=task.task_name,
                        created_at=task.created_at, updated_at=task.updated_at)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return Task(id=TaskId(id=db_task.id), user_id=UserId(id=db_task.user_id), task_name=db_task.task_name,
                created_at=db_task.created_at, updated_at=db_task.updated_at)


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
