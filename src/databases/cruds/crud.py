
from sqlalchemy.orm import Session

from ..models import user
from ...schemas import schemas

def get_user(db: Session, user_id: int):
    return db.query(user.User).filter(user.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(user.User).filter(user.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = user.password  # Here you should hash the password
    db_user = user.User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: schemas.User):
    db_user = db.query(user.User).filter(user.User.id == user.id).first()
    db_user.name = user.name
    db_user.email = user.email
    db_user.hashed_password = user.hashed_password
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(user.User).filter(user.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user
