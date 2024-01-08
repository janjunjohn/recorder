from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    password: str
    username: str
    email: str


class UserPasswordUpdateRequest(BaseModel):
    password: str
    old_password: str


class UserUpdateRequest(BaseModel):
    username: str
    email: str
