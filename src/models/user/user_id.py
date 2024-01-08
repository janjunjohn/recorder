import uuid
from pydantic import BaseModel, field_validator
from services.common.errors import InvalidUUIDError


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
