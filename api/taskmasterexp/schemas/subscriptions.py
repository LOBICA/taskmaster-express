from pydantic import BaseModel


class SubscriptionData(BaseModel):
    status: bool


class SubscriptionResponse(SubscriptionData):
    pass
