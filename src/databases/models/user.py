from sqlalchemy import Column, Integer, String
from src.databases.settings.database import Base

class User(Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    hashed_password = Column(String)
