from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from databases.settings.database import get_db
from schemas.user_schema import UserCreateRequest, UserPasswordUpdateRequest, UserUpdateRequest
from services.common.errors import UserAlreadyExistsError, UserNotFoundError, PasswordNotMatchError, InvalidUUIDError, ValidationError
from services import user_service
from models.user.user_id import UserId
from models.user.user import User


router = APIRouter(prefix='/users', tags=['users'])


@router.post("/")
def signup(user: UserCreateRequest, db: Session = Depends(get_db)) -> User:
    try:
        return user_service.create_user(db, user)
    except (UserAlreadyExistsError, ValidationError) as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)) -> None:
    try:
        return user_service.delete_user(db, UserId(id=user_id))
    except InvalidUUIDError as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.get("/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)) -> User:
    try:
        return user_service.get_user_by_id(db, UserId(id=user_id))
    except InvalidUUIDError as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.put("/{user_id}")
def update_password(user_id: str, user_password_update: UserPasswordUpdateRequest, db: Session = Depends(get_db)) -> None:
    try:
        return user_service.update_password(db, UserId(id=user_id), user_password_update)
    except (InvalidUUIDError, PasswordNotMatchError, ValidationError) as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.put("/{user_id}")
def update_user(user_id: str, new_user_info: UserUpdateRequest, db: Session = Depends(get_db)) -> None:
    try:
        return user_service.update_user(db, UserId(id=user_id), new_user_info)
    except (InvalidUUIDError, ValidationError) as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
