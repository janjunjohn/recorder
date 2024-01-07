import uuid
import datetime
from sqlalchemy.orm import Session

from databases.cruds import user_crud
from schemas.user_schema import UserCreateRequest, UserPasswordUpdateRequest, UserUpdateRequest
from services.common.errors import UserAlreadyExistsError, UserNotFoundError, PasswordNotMatchError
from services.common.hash import HashService
from models.user.user_id import UserId
from models.user.user import User
from src.models.user.user_password import UserPassword


def get_user_by_email(db: Session, email: str) -> User:
    return user_crud.get_user_by_email(db, email)


def get_user_by_id(db: Session, user_id: UserId) -> User:
    return user_crud.get_user_by_id(db, user_id)


def create_user(db: Session, user: UserCreateRequest) -> User:
    exists_user: bool = user_crud.exists_user_by_email(db, user.email)
    if exists_user:
        raise UserAlreadyExistsError("このemailはすでに存在します")

    user_password: UserPassword = UserPassword(password=user.password)

    hashed_password: str = HashService.get_password_hash(user_password.value)

    user: User = User(
        id=UserId(id=uuid.uuid4()),
        email=user.email,
        username=user.username,
        is_active=True,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )

    return user_crud.create_user(db, user, hashed_password)


def delete_user(db: Session, user_id: UserId) -> None:
    exists_user: bool = user_crud.exists_active_user_by_id(db, user_id)
    if not exists_user:
        raise UserNotFoundError("ユーザーが見つかりませんでした")

    user_crud.delete_user(db, user_id)


def update_password(db: Session, user_id: UserId, user_password_update: UserPasswordUpdateRequest) -> None:
    user_password: UserPassword = user_crud.get_user_password_by_id(
        db, user_id)
    old_password: UserPassword = UserPassword(
        password=user_password_update.old_password)
    if not HashService.verify_password(old_password.value, user_password.value):
        raise PasswordNotMatchError("パスワードが一致しませんでした")
    new_password: UserPassword = UserPassword(
        password=user_password_update.password)
    hashed_password: str = HashService.get_password_hash(
        new_password.value)

    # updated_atの更新
    user: User = get_user_by_id(db, user_id)
    updated_user = User(
        id=user.id.id,
        email=user.email,
        username=user.username,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=datetime.datetime.now()
    )

    user_crud.update_user(db, updated_user, hashed_password)


def update_user(db: Session, user_id: UserId, user_info: UserUpdateRequest) -> None:
    user: User = get_user_by_id(db, user_id)

    user = User(
        id=user.id.id,
        email=user_info.email,
        username=user_info.username,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=datetime.datetime.now()
    )
    user_crud.update_user(db, user)
