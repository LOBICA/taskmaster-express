from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserData(BaseModel):
    name: str
    email: str | None = None
    phone_number: str | None = None


class User(UserData):
    uuid: UUID | None = None

    model_config = ConfigDict(from_attributes=True)


class UserRegisterInput(UserData):
    email: str
    password: str


class UserResponse(UserData):
    uuid: UUID


class PasswordInput(BaseModel):
    password: str
    new_password: str = Field(alias="newPassword")
