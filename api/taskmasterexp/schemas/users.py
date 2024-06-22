from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    uuid: UUID
    name: str
    email: str | None

    class Config:
        orm_mode = True
