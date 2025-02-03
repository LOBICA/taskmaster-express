from uuid import UUID

from pydantic import BaseModel, Field


class SubscriptionData(BaseModel):
    is_active: bool = Field(..., alias="isActive")

    class Config:
        populate_by_name = True


class SubscriptionResponse(SubscriptionData):
    pass


class Subscription(SubscriptionData):
    uuid: UUID
    user_id: UUID | None
    subscription_id: str
    plan_id: str | None

    class Config:
        from_attributes = True
        populate_by_name = True


class SubscriptionPayload(BaseModel):
    subscription_id: str = Field(..., alias="subscriptionId")
