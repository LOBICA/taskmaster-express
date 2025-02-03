from fastapi import APIRouter, status

from taskmaster.auth.dependencies import CurrentUser
from taskmaster.database.dependencies import SubscriptionManager
from taskmaster.paypal.dependencies import PayPalClient
from taskmaster.schemas.subscriptions import (
    SubscriptionPayload,
    SubscriptionResponse,
)
from taskmaster.settings import PAYPAL_PRODUCT_ID

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
        return SubscriptionResponse(**subscription.model_dump())
    return SubscriptionResponse(is_active=False)


@router.post("/link", response_model=SubscriptionResponse)
async def link_subscription_to_user(
    current_user: CurrentUser,
    subscriptions_manager: SubscriptionManager,
    payload: SubscriptionPayload,
):
    subscription = await subscriptions_manager.link_subscription(
        current_user.uuid, payload.subscription_id
    )
    return SubscriptionResponse(**subscription.model_dump())


@router.post("/cancel", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_subscription(
    current_user: CurrentUser,
    subscriptions_manager: SubscriptionManager,
    paypal_client: PayPalClient,
):
    subscription = await subscriptions_manager.get_active_subscription(
        current_user.uuid
    )
    await paypal_client.cancel_subscription(subscription.subscription_id)
    await subscriptions_manager.cancel_subscription(subscription.subscription_id)


@router.get("/plans")
async def get_plans(paypal_client: PayPalClient):
    return paypal_client.list_subscription_plans(PAYPAL_PRODUCT_ID)
