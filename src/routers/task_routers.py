from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from databases.settings.database import get_db
from services.common.errors import TaskAlreadyExistsError, TaskNotFoundError, InvalidUUIDError, ValidationError
from services import task_service
from models.user.user_id import UserId
from models.task.task import Task


router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post("/{user_id}")
def create_task(user_id: str, task_name, db: Session = Depends(get_db)) -> Task:
    try:
        return task_service.create_task(db, UserId(id=user_id), task_name)
    except (TaskAlreadyExistsError, ValidationError, InvalidUUIDError) as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.get("/{user_id}")
def get_task_list(user_id: str, db: Session = Depends(get_db)) -> List[Task]:
    try:
        return task_service.get_task_list_by_user_id(db, UserId(id=user_id))
    except InvalidUUIDError as e:
        raise HTTPException(status_code=400, detail=e.args[0])
