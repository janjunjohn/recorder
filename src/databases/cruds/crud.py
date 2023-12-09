from sqlalchemy.orm import Session

from databases.models.user import User as UserTable
from schemas.user_schema import UserCreate, User
from services.common.hash import HashService

# def get_user(db: Session, user_id: int):
#     return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(UserTable).filter(UserTable.email == email).first()

# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password: str = HashService.get_password_hash(user.password)  
    db_user = UserTable(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# def update_user(db: Session, user: UserSchema):
#     db_user = db.query(User).filterx(User.id == user.id).first()
#     db_user.name = user.name
#     db_user.email = user.email
#     db_user.hashed_password = user.hashed_password
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def delete_user(db: Session, user_id: int):
#     db_user = db.query(User).filter(User.id == user_id).first()
#     db.delete(db_user)
#     db.commit()
#     return db_user
