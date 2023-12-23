import uuid
import datetime
from pydantic import BaseModel, field_validator
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str

    @field_validator('username')
    def username_is_valid(cls, username: str) -> str:
        if len(username) < 3:
            raise ValueError('ユーザー名は3文字以上にしてください。')
        if len(username) > 20:
            raise ValueError('ユーザー名は20文字以下にしてください。')
        return username

    @field_validator('email')
    def email_is_valid(cls, email: str) -> str:
        if '@' not in email:
            raise ValueError('メールアドレスの形式が正しくありません。')
        return email


class UserCreate(UserBase):
    password: str

    @field_validator('password')
    def password_is_valid(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError('パスワードは8文字以上にしてください。')
        if len(password) > 20:
            raise ValueError('パスワードは20文字以下にしてください。')
        return password


class User(UserBase):
    id: str | uuid.UUID
    hashed_password: str
    is_active: bool
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True

    @field_validator('id')
    def id_is_valid(cls, id: str) -> str:
        try:
            uuid.UUID(id)
        except ValueError:
            raise ValueError('IDの形式が正しくありません。')
        return id


class UserPasswordUpdate(BaseModel):
    password: str
    old_password: str

    @field_validator('password')
    def password_is_valid(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError('パスワードは8文字以上にしてください。')
        if len(password) > 20:
            raise ValueError('パスワードは20文字以下にしてください。')
        return password
