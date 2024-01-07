from pydantic import BaseModel, field_validator
from services.common.errors import ValidationError


class UserPassword(BaseModel):
    value: str

    @field_validator('value')
    def value_is_valid(cls, password: str) -> str:
        if len(password) < 8:
            raise ValidationError('パスワードは8文字以上にしてください。')
        if len(password) > 20:
            raise ValidationError('パスワードは20文字以下にしてください。')
        return password
