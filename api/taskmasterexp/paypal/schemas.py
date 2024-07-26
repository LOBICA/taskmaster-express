from pydantic import BaseModel, Field


class Product(BaseModel):
    id_: str
    name: str
    description: str
