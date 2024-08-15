from pydantic import BaseModel, Field


class SubscriptionData(BaseModel):
    is_active: bool = Field(..., alias="isActive")
    class Config:
        allow_population_by_field_name = True


class SubscriptionResponse(SubscriptionData):
    pass
