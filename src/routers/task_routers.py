from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from databases.settings.database import get_db
from schemas.task_schema import TaskCreate, Task
from services.common.errors import TaskAlreadyExistsError, TaskNotFoundError
from services import task_service


router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post("/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)) -> Task:
    try:
        return task_service.create_task(db, task)
    except (TaskAlreadyExistsError, ValueError) as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
