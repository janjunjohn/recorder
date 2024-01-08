from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from databases.models.user import User as UserTable
from models.user.user_id import UserId
from models.user.user import User
from src.models.user.user_password import UserPassword
from services.common.errors import UserNotFoundError


def get_user_by_id(db: Session, user_id: UserId) -> User:
    try:
        db_user = db.query(UserTable).filter(UserTable.id == user_id.id).one()
        return User(id=UserId(id=db_user.id), email=db_user.email, username=db_user.username,
                    is_active=db_user.is_active, created_at=db_user.created_at, updated_at=db_user.updated_at)
    except NoResultFound:
        raise UserNotFoundError("ユーザーが見つかりませんでした")


def get_user_by_email(db: Session, email: str) -> User:
    try:
        db_user: UserTable = db.query(UserTable).filter(
            UserTable.email == email).one()
        return User(id=UserId(id=db_user.id), email=db_user.email, username=db_user.username,
                    is_active=db_user.is_active, created_at=db_user.created_at, updated_at=db_user.updated_at)
    except NoResultFound:
        raise UserNotFoundError("ユーザーが見つかりませんでした")


def get_user_password_by_id(db: Session, user_id: UserId) -> UserPassword:
    try:
        db_user = db.query(UserTable).filter(UserTable.id == user_id.id).one()
        return UserPassword(value=db_user.hashed_password)
    except NoResultFound:
        raise UserNotFoundError("ユーザーが見つかりませんでした")


def exists_active_user_by_id(db: Session, user_id: UserId) -> bool:
    query = db.query(UserTable).filter(
        UserTable.id == user_id.id, UserTable.is_active == True)
    return db.query(query.exists()).scalar()


def exists_user_by_email(db: Session, email: str) -> bool:
    query = db.query(UserTable).filter(UserTable.email == email)
    return db.query(query.exists()).scalar()


def delete_user(db: Session, user_id: UserId) -> None:
    db_user = db.query(UserTable).filter(UserTable.id == user_id.id).one()
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)


def create_user(db: Session, user: User, new_password: str) -> User:
    db_user = UserTable(id=user.id.id, email=user.email, username=user.username, hashed_password=new_password,
                        is_active=user.is_active, created_at=user.created_at, updated_at=user.updated_at)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User(id=UserId(id=db_user.id), email=db_user.email, username=db_user.username,
                is_active=db_user.is_active, created_at=db_user.created_at, updated_at=db_user.updated_at)


def update_user(db: Session, user: User) -> User:
    db_user = db.query(UserTable).filter(UserTable.id == user.id.id).one()
    db_user.email = user.email
    db_user.username = user.username
    db_user.updated_at = user.updated_at
    db.commit()
    db.refresh(db_user)
    return User(id=UserId(id=db_user.id), email=db_user.email, username=db_user.username,
                is_active=db_user.is_active, created_at=db_user.created_at, updated_at=db_user.updated_at)


def update_password(db: Session, user: User, new_password: str) -> None:
    db_user = db.query(UserTable).filter(UserTable.id == user.id.id).one()
    db_user.hashed_password = new_password
    db_user.updated_at = user.updated_at
    db.commit()
    db.refresh(db_user)
