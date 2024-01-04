import uuid
import datetime
from pydantic import BaseModel, field_validator
from typing import Optional
from services.common.errors import InvalidUUIDError, ValidationError


class UserBase(BaseModel):
    username: str
    email: str


class UserId(BaseModel):
    id: str | uuid.UUID

    @field_validator('id')
    def id_is_valid(cls, value: str | uuid.UUID) -> str:
        if isinstance(value, uuid.UUID):
            return str(value)
        try:
            return str(uuid.UUID(value))
        except ValueError:
            raise InvalidUUIDError('IDの形式が正しくありません。')


class UserPassword(BaseModel):
    password: str

    @field_validator('password')
    def password_is_valid(cls, password: str) -> str:
        if len(password) < 8:
            raise ValidationError('パスワードは8文字以上にしてください。')
        if len(password) > 20:
            raise ValidationError('パスワードは20文字以下にしてください。')
        return password


class User(UserBase):
    id: UserId
    hashed_password: str
    is_active: bool
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True

    @field_validator('username')
    def username_is_valid(cls, username: str) -> str:
        if len(username) < 3:
            raise ValidationError('ユーザー名は3文字以上にしてください。')
        if len(username) > 20:
            raise ValidationError('ユーザー名は20文字以下にしてください。')
        return username

    @field_validator('email')
    def email_is_valid(cls, email: str) -> str:
        if '@' not in email:
            raise ValidationError('メールアドレスの形式が正しくありません。')
        return email


class UserCreate(UserBase):
    password: str


class UserPasswordUpdate(BaseModel):
    password: str
    old_password: str
