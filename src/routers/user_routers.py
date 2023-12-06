from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from databases.cruds import crud
from databases.settings.database import get_db
from schemas.user_schema import UserCreate, User


router = APIRouter(prefix='/users', tags=['users'])


@router.post("/")
def signup(user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user: User = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="ユーザーがすでに存在します")

    return crud.create_user(db=db, user=user)