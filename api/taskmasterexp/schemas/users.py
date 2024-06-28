from uuid import UUID

from pydantic import BaseModel, Field


class UserData(BaseModel):
    name: str
    email: str | None


class User(UserData):
    uuid: UUID | None = None

    class Config:
        orm_mode = True


class UserRegisterInput(UserData):
    email: str
    password: str


class UserResponse(UserData):
    uuid: UUID


class PasswordInput(BaseModel):
    password: str
    new_password: str = Field(alias="newPassword")
