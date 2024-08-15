from fastapi import APIRouter, status

from taskmasterexp.auth.dependencies import CurrentUser
from taskmasterexp.database.dependencies import SubscriptionManager
from taskmasterexp.paypal.dependencies import PayPalClient
from taskmasterexp.schemas.subscriptions import (
    SubscriptionPayload,
    SubscriptionResponse,
)

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.get("/status", response_model=SubscriptionResponse)
async def get_subscription_status(
    current_user: CurrentUser,
    subscriptions_manager: SubscriptionManager,
):
    subscription = await subscriptions_manager.get_active_subscription(
        current_user.uuid
    )
    if subscription:
        return SubscriptionResponse(**subscription.dict())
    return SubscriptionResponse(is_active=False)


@router.post("/activate", response_model=SubscriptionResponse)
async def activate_subscription(
    current_user: CurrentUser,
    subscriptions_manager: SubscriptionManager,
    payload: SubscriptionPayload,
):
    subscription = await subscriptions_manager.add_subscription(
        current_user.uuid, payload.order_id
    )
    return SubscriptionResponse(**subscription.dict())


@router.post("/cancel", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_subscription(
    current_user: CurrentUser,
    subscriptions_manager: SubscriptionManager,
    paypal_client: PayPalClient,
):
    subscription = await subscriptions_manager.get_active_subscription(
        current_user.uuid
    )
    await paypal_client.cancel_subscription(subscription.order_id)
    await subscriptions_manager.cancel_subscription(current_user.uuid)
