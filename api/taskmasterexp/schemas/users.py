from uuid import UUID

from pydantic import BaseModel


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
