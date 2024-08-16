import logging

from fastapi import APIRouter, HTTPException, Request, status

from taskmasterexp.database.dependencies import SubscriptionManager

from .dependencies import PayPalClient
from .schemas import EventType, WebhookData

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/paypal/webhooks", tags=["paypal"])


@router.post("/subscription")
async def subscription_webhook(
    paypal_client: PayPalClient,
    subscription_manager: SubscriptionManager,
    request: Request,
    data: WebhookData,
):
    body = await request.body()
    logger.info(body)

    transmission_id = request.headers.get("paypal-transmission-id")
    timestamp = request.headers.get("paypal-transmission-time")
    cert_url = request.headers.get("paypal-cert-url")
    auth_algo = request.headers.get("paypal-auth-algo")
    transmission_sig = request.headers.get("paypal-transmission-sig")

    verification = paypal_client.verify_paypal_webhook(
        transmission_id=transmission_id,
        timestamp=timestamp,
        cert_url=cert_url,
        auth_algo=auth_algo,
        transmission_sig=transmission_sig,
        body=body,
    )
    if not verification:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if data.event_type == EventType.SUBSCRIPTION_ACTIVATED:
        await subscription_manager.activate_subscription(
            data.resource.id, data.resource.plan_id
        )

    if data.event_type in {
        EventType.SUBSCRIPTION_CANCELLED,
        EventType.SUBSCRIPTION_SUSPENDED,
        EventType.SUBSCRIPTION_EXPIRED,
    }:
        await subscription_manager.cancel_subscription(data.resource.id)

    return {"status": "ok"}
