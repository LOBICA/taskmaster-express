from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    uuid: UUID
    email: str

    class Config:
        orm_mode = True
