from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from databases.settings.database import get_db
from schemas.user_schema import UserCreate, User, UserPasswordUpdate, UserBase, UserId
from services.common.errors import UserAlreadyExistsError, UserNotFoundError, PasswordNotMatchError, InvalidUUIDError
from services import user_service


router = APIRouter(prefix='/users', tags=['users'])


@router.post("/")
def signup(user: UserCreate, db: Session = Depends(get_db)) -> User:
    try:
        return user_service.create_user(db, user)
    except (UserAlreadyExistsError, ValueError) as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)) -> None:
    try:
        return user_service.delete_user(db, UserId(id=user_id))
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.get("/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)) -> User:
    try:
        return user_service.get_user_by_id(db, UserId(id=user_id))
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.put("/{user_id}")
def update_password(user_id: str, user_password_update: UserPasswordUpdate, db: Session = Depends(get_db)) -> None:
    try:
        return user_service.update_password(db, UserId(id=user_id), user_password_update)
    except (ValueError, PasswordNotMatchError) as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.put("/{user_id}")
def update_user(user_id: str, user_info: UserBase, db: Session = Depends(get_db)) -> None:
    try:
        return user_service.update_user(db, UserId(id=user_id), user_info)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
