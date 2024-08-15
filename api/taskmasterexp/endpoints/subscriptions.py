from fastapi import APIRouter

from taskmasterexp.auth.dependencies import CurrentUser
from taskmasterexp.schemas.subscriptions import SubscriptionResponse

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.get("/status", response_model=SubscriptionResponse)
async def get_subscription_status(current_user: CurrentUser):
    return SubscriptionResponse(is_active=False)


@router.post("/activate", response_model=SubscriptionResponse)
async def activate_subscription(current_user: CurrentUser):
    return SubscriptionResponse(is_active=True)


@router.post("/cancel", response_model=SubscriptionResponse)
async def cancel_subscription(current_user: CurrentUser):
    return SubscriptionResponse(is_active=False)
