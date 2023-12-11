import uuid
import datetime
from typing import Optional
from sqlalchemy.orm import Session
from databases.cruds import crud
from schemas.user_schema import User, UserCreate, UserPasswordUpdate, UserBase
from services.common.errors import UserAlreadyExistsError, UserNotFoundError, PasswordNotMatchError
from services.common.hash import HashService


def get_user_by_email(db: Session, email: str) -> User:
    return crud.get_user_by_email(db, email)


def get_user_by_id(db: Session, user_id: str) -> User:
    user: Optional[User] = crud.get_user_by_id(db, user_id)
    return user


def create_user(db: Session, user: UserCreate) -> User:
    exists_user: bool = crud.exists_user_by_email(db, user.email)
    if exists_user:
        raise UserAlreadyExistsError("このemailはすでに存在します")
    hashed_password: str = HashService.get_password_hash(user.password)

    user: User = User(
        id=uuid.uuid4(),
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        is_active=True,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )

    return crud.create_user(db, user)


def delete_user(db: Session, user_id: str) -> None:
    exists_user: bool = crud.exists_active_user_by_id(db, user_id)
    if not exists_user:
        raise UserNotFoundError("ユーザーが見つかりませんでした")

    return crud.delete_user(db, user_id)


def update_password(db: Session, user_id: str, user_password_update: UserPasswordUpdate) -> None:
    user: User = get_user_by_id(db, user_id)
    if not HashService.verify_password(user_password_update.old_password, user.hashed_password):
        raise PasswordNotMatchError("パスワードが一致しませんでした")

    hashed_password: str = HashService.get_password_hash(
        user_password_update.password)

    user = User(
        id=user.id,
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=datetime.datetime.now()
    )
    crud.update_user(db, user)


def update_user(db: Session, user_id: str, user_info: UserBase) -> None:
    user: User = get_user_by_id(db, user_id)

    user = User(
        id=user.id,
        email=user_info.email,
        username=user_info.username,
        hashed_password=user.hashed_password,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=datetime.datetime.now()
    )
    crud.update_user(db, user)
