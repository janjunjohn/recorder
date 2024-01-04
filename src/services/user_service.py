import uuid
import datetime
from sqlalchemy.orm import Session

from databases.cruds import user_crud
from schemas.user_schema import User, UserCreate, UserPasswordUpdate, UserBase, UserId
from services.common.errors import UserAlreadyExistsError, UserNotFoundError, PasswordNotMatchError
from services.common.hash import HashService
from schemas.user_schema import UserPassword


def get_user_by_email(db: Session, email: str) -> User:
    return user_crud.get_user_by_email(db, email)


def get_user_by_id(db: Session, user_id: UserId) -> User:
    return user_crud.get_user_by_id(db, user_id)


def create_user(db: Session, user: UserCreate) -> User:
    exists_user: bool = user_crud.exists_user_by_email(db, user.email)
    if exists_user:
        raise UserAlreadyExistsError("このemailはすでに存在します")

    password: UserPassword = UserPassword(password=user.password)

    hashed_password: str = HashService.get_password_hash(password)
    user: User = User(
        id=UserId(id=uuid.uuid4()),
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        is_active=True,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )

    return user_crud.create_user(db, user)


def delete_user(db: Session, user_id: UserId) -> None:
    exists_user: bool = user_crud.exists_active_user_by_id(db, user_id)
    if not exists_user:
        raise UserNotFoundError("ユーザーが見つかりませんでした")

    return user_crud.delete_user(db, user_id)


def update_password(db: Session, user_id: UserId, user_password_update: UserPasswordUpdate) -> None:
    user: User = get_user_by_id(db, user_id)
    old_password: UserPassword = UserPassword(
        password=user_password_update.old_password)
    new_password: UserPassword = UserPassword(
        password=user_password_update.password)

    if not HashService.verify_password(old_password, user.hashed_password):
        raise PasswordNotMatchError("パスワードが一致しませんでした")

    hashed_password: str = HashService.get_password_hash(
        user_password_update.password)

    user = User(
        id=UserId(id=user.id),
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=datetime.datetime.now()
    )
    user_crud.update_user(db, user)


def update_user(db: Session, user_id: UserId, user_info: UserBase) -> None:
    user: User = get_user_by_id(db, user_id)

    user = User(
        id=user.id.id,
        email=user_info.email,
        username=user_info.username,
        hashed_password=user.hashed_password,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=datetime.datetime.now()
    )
    user_crud.update_user(db, user)
