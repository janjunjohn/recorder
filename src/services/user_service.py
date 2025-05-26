import uuid
from sqlalchemy.orm import Session

from databases.cruds import user_crud
from schemas.user_schema import UserCreateRequest, UserPasswordUpdateRequest, UserUpdateRequest
from services.common.errors import UserAlreadyExistsError, UserNotFoundError, PasswordNotMatchError
from services.common.hash import HashService
from models.user.user_id import UserId
from models.user.user import User
from models.user.user_password import UserPassword


def create_user(db: Session, user_create: UserCreateRequest) -> User:
    exists_user: bool = user_crud.exists_user_by_email(db, user_create.email)
    if exists_user:
        raise UserAlreadyExistsError("このemailはすでに存在します")

    user_password: UserPassword = UserPassword(password=user_create.password)

    hashed_password: str = HashService.get_password_hash(user_password.value)

    user: User = User(
        id=UserId(id=uuid.uuid4()),
        email=user_create.email,
        username=user_create.username,
        is_active=True,
    )

    return user_crud.create_user(db, user, hashed_password)


def get_user_by_id(db: Session, user_id: UserId) -> User:
    return user_crud.get_user_by_id(db, user_id)


def get_user_by_email(db: Session, email: str) -> User:
    return user_crud.get_user_by_email(db, email)


def update_password(db: Session, user_id: UserId, user_password_update: UserPasswordUpdateRequest) -> None:
    user_password: UserPassword = user_crud.get_user_password_by_id(db, user_id)
    old_password: UserPassword = UserPassword(
        password=user_password_update.old_password)
    if not HashService.verify_password(old_password.value, user_password.value):
        raise PasswordNotMatchError("パスワードが一致しませんでした")
    new_password: UserPassword = UserPassword(
        password=user_password_update.password)
    hashed_password: str = HashService.get_password_hash(
        new_password.value)

    user_crud.update_password(db, user_id, hashed_password)


def update_user(db: Session, user_id: UserId, user_update: UserUpdateRequest) -> None:
    user: User = get_user_by_id(db, user_id)

    updated_user = User(
        id=UserId(id=user.id),
        email=user_update.email,
        username=user_update.username,
    )
    user_crud.update_user(db, updated_user)


def delete_user(db: Session, user_id: UserId) -> None:
    exists_user: bool = user_crud.exists_active_user_by_id(db, user_id)
    if not exists_user:
        raise UserNotFoundError("ユーザーが見つかりませんでした")

    user_crud.delete_user(db, user_id)
