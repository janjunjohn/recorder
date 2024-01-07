import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
from services.common.errors import ValidationError
from models.user.user_id import UserId


class User(BaseModel):
    id: UserId
    username: str
    email: str
    is_active: bool
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

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
