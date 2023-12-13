from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from databases.models.user import User as UserTable
from schemas.user_schema import User
from services.common.errors import UserNotFoundError


def get_user_by_id(db: Session, user_id: str) -> User:
    try:
        db_user: User = db.query(UserTable).filter(UserTable.id == user_id).one()
        return User(id=db_user.id, email=db_user.email, username=db_user.username, hashed_password=db_user.hashed_password, is_active=db_user.is_active, created_at=db_user.created_at, updated_at=db_user.updated_at)
    except NoResultFound as e:
        raise UserNotFoundError("ユーザーが見つかりませんでした")



def get_user_by_email(db: Session, email: str) -> User:
    try:
        db_user: UserTable = db.query(UserTable).filter(
            UserTable.email == email).one()
        return User(id=db_user.id, email=db_user.email, username=db_user.username, hashed_password=db_user.hashed_password, is_active=db_user.is_active, created_at=db_user.created_at, updated_at=db_user.updated_at)
    except NoResultFound as e:
        raise UserNotFoundError("ユーザーが見つかりませんでした")

def exists_active_user_by_id(db: Session, user_id: str) -> bool:
    query = db.query(UserTable).filter(
        UserTable.id == user_id, UserTable.is_active == True)
    return db.query(query.exists()).scalar()


def exists_user_by_email(db: Session, email: str) -> bool:
    query = db.query(UserTable).filter(UserTable.email == email)
    return db.query(query.exists()).scalar()


def delete_user(db: Session, user_id: str) -> None:
    db_user = db.query(UserTable).filter(UserTable.id == user_id).one()
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)


def create_user(db: Session, user: User) -> User:
    db_user = UserTable(id=user.id, email=user.email, username=user.username,
                        hashed_password=user.hashed_password, is_active=user.is_active, created_at=user.created_at, updated_at=user.updated_at)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User(id=db_user.id, email=db_user.email, username=db_user.username, hashed_password=db_user.hashed_password, is_active=db_user.is_active, created_at=db_user.created_at, updated_at=db_user.updated_at)


def update_user(db: Session, user: User) -> User:
    db_user = db.query(UserTable).filter(UserTable.id == user.id).one()
    db_user.email = user.email
    db_user.username = user.username
    db_user.hashed_password = user.hashed_password
    db_user.is_active = user.is_active
    db_user.updated_at = user.updated_at
    db.commit()
    db.refresh(db_user)
    return User(id=db_user.id, email=db_user.email, username=db_user.username, hashed_password=db_user.hashed_password, is_active=db_user.is_active, created_at=db_user.created_at, updated_at=db_user.updated_at)