from pydantic import BaseModel
from uuid import UUID


class User(BaseModel):
    uuid: UUID
    email: str

    class Config:
        orm_mode = True
