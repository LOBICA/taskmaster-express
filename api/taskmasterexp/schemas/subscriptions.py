from uuid import UUID

from pydantic import BaseModel, Field


class SubscriptionData(BaseModel):
    is_active: bool = Field(..., alias="isActive")

    class Config:
        allow_population_by_field_name = True


class SubscriptionResponse(SubscriptionData):
    pass


class Subscription(SubscriptionData):
    uuid: UUID
    user_id: UUID | None
    order_id: str
    plan_id: str | None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class SubscriptionPayload(BaseModel):
    order_id: str = Field(..., alias="orderId")
