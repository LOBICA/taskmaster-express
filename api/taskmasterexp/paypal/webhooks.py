import logging

from fastapi import APIRouter, HTTPException, Request, status

from taskmasterexp.settings import PAYPAL_WEBHOOK_ID

from .client import PayPalClient

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/paypal/webhooks", tags=["paypal"])


@router.post("/subscription")
async def subscription_webhook(request: Request):
    client = PayPalClient.get_client()
    body = await request.body()
    # logger.info(body)

    transmission_id = request.headers.get("paypal-transmission-id")
    timestamp = request.headers.get("paypal-transmission-time")
    cert_url = request.headers.get("paypal-cert-url")
    auth_algo = request.headers.get("paypal-auth-algo")
    transmission_sig = request.headers.get("paypal-transmission-sig")

    verification = client.verify_paypal_webhook(
        transmission_id=transmission_id,
        timestamp=timestamp,
        cert_url=cert_url,
        auth_algo=auth_algo,
        transmission_sig=transmission_sig,
        body=body,
    )
    if not verification:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return {"status": "ok"}
