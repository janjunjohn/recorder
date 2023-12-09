from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from databases.settings.database import get_db
from schemas.user_schema import UserCreate, User
from services.common.errors import UserAlreadyExistsError
from services.user_service import create_user


router = APIRouter(prefix='/users', tags=['users'])


@router.post("/")
def signup(user: UserCreate, db: Session = Depends(get_db)) -> User:
    try:
        return create_user(db, user)
    except UserAlreadyExistsError as e:
        print(e)
        return HTTPException(status_code=400, detail=e.args[0])
    except Exception as e:
        return HTTPException(status_code=500, detail=e)
