from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from databases.settings.database import get_db
from services.common.errors import TaskAlreadyExistsError, TaskNotFoundError, InvalidUUIDError, ValidationError
from services import task_service
from models.user.user_id import UserId
from models.task.task import Task
from schemas.task_schema import TaskCreateRequest, TaskNameUpdateRequest


router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post("/{user_id}")
def create_task(user_id: str, task_create: TaskCreateRequest, db: Session = Depends(get_db)) -> Task:
    try:
        return task_service.create_task(db, UserId(id=user_id), task_create)
    except (TaskAlreadyExistsError, ValidationError, InvalidUUIDError) as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.get("/{user_id}/{task_id}")
def get_task(user_id: str, task_id: str, db: Session = Depends(get_db)) -> Task:
    try:
        return task_service.get_task_by_id(user_id, task_id, db)
    except (TaskNotFoundError, InvalidUUIDError) as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.get("/{user_id}")
def get_task_list(user_id: str, db: Session = Depends(get_db)) -> List[Task]:
    try:
        return task_service.get_task_list_by_user_id(db, UserId(id=user_id))
    except InvalidUUIDError as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@router.post("/{user_id}/{task_id}")
def update_task_name(user_id: str, task_id: str, task_name_update: TaskNameUpdateRequest, db: Session = Depends(get_db)) -> Task:
    try:
        return task_service.update_task_name(db, user_id, task_id, task_name_update)
    except (TaskNotFoundError, TaskAlreadyExistsError, ValidationError, InvalidUUIDError) as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.post("/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)) -> None:
    try:
        return task_service.delete_task(db, task_id)
    except (TaskNotFoundError, InvalidUUIDError) as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
