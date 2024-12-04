import json
import logging
from datetime import datetime, timedelta
from typing import Self

import httpx

from taskmasterexp.settings import (
    PAYPAL_API_URL,
    PAYPAL_CLIENT_ID,
    PAYPAL_SECRET_KEY,
    PAYPAL_WEBHOOK_ID,
)

from .schemas import Product, SubscriptionPlan, SubscriptionPlanData

logger = logging.getLogger(__name__)


class PayPalClient:
    _access_token = None
    _expiration_time = None

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    @classmethod
    def get_client(cls) -> Self:
        return cls(client_id=PAYPAL_CLIENT_ID, client_secret=PAYPAL_SECRET_KEY)

    @property
    def token(self) -> str:
        if self._access_token is None or datetime.now() > self._expiration_time:
            data = self._get_access_token_data()
            self._access_token = data["access_token"]
            self._expiration_time = datetime.now() + timedelta(
                seconds=data["expires_in"]
            )
        return self._access_token

    def _get_access_token_data(self) -> dict:
        url = f"{PAYPAL_API_URL}/v1/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "client_credentials",
        }
        response = httpx.post(
            url, headers=headers, data=data, auth=(self.client_id, self.client_secret)
        )
        response.raise_for_status()
        return response.json()

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def list_products(self) -> list[Product]:
        headers = self._get_headers()
        url = f"{PAYPAL_API_URL}/v1/catalogs/products"
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        logger.info(data)
        return [
            Product(
                id_=product["id"],
                name=product["name"],
                description=product["description"],
            )
            for product in data["products"]
        ]

    def create_product(self, name: str, description: str) -> str:
        headers = self._get_headers()
        url = f"{PAYPAL_API_URL}/v1/catalogs/products"

        product = {
            "name": name,
            "description": description,
            "type": "SERVICE",
            "category": "SOFTWARE",
        }

        response = httpx.post(url, headers=headers, json=product)
        response.raise_for_status()
        data = response.json()
        return data["id"]

    def list_subscription_plans(self, product_id: str) -> list[SubscriptionPlan]:
        headers = self._get_headers()
        url = f"{PAYPAL_API_URL}/v1/billing/plans?product_id={product_id}"
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return [
            SubscriptionPlan(
                product_id=product_id,
                id_=plan["id"],
                name=plan["name"],
                description=plan["description"],
                status=plan["status"],
            )
            for plan in data["plans"]
        ]

    def create_subscription_plan(
        self,
        product_id: str,
        name: str,
        description: str,
        monthly_price: str,
        trial_months: int = 0,
    ) -> str:
        billing_cycles = []
        if trial_months:
            billing_cycles.append(
                {
                    "frequency": {
                        "interval_unit": "MONTH",
                        "interval_count": 1,
                    },
                    "tenure_type": "TRIAL",
                    "sequence": 1,
                    "total_cycles": trial_months,
                }
            )

        billing_cycles.append(
            {
                "frequency": {
                    "interval_unit": "MONTH",
                    "interval_count": 1,
                },
                "tenure_type": "REGULAR",
                "sequence": 2 if trial_months else 1,
                "total_cycles": 0,
                "pricing_scheme": {
                    "fixed_price": {
                        "currency_code": "USD",
                        "value": monthly_price,
                    }
                },
            }
        )

        subscription_plan = SubscriptionPlanData(
            product_id=product_id,
            name=name,
            description=description,
            billing_cycles=billing_cycles,
            payment_preferences={
                "auto_bill_outstanding": True,
                "payment_failure_threshold": 3,
            },
        )

        headers = self._get_headers()
        url = f"{PAYPAL_API_URL}/v1/billing/plans"
        response = httpx.post(url, headers=headers, json=subscription_plan.model_dump())
        try:
            response.raise_for_status()
        except Exception:
            logger.error(response.text)
            raise
        data = response.json()
        return data["id"]

    def verify_paypal_webhook(
        self,
        transmission_id: str,
        timestamp: str,
        cert_url: str,
        auth_algo: str,
        transmission_sig: str,
        body: bytes,
    ):
        data = {
            "transmission_id": transmission_id,
            "transmission_time": timestamp,
            "cert_url": cert_url,
            "auth_algo": auth_algo,
            "transmission_sig": transmission_sig,
            "webhook_id": PAYPAL_WEBHOOK_ID,
            "webhook_event": "[BODY]",
        }
        json_data = json.dumps(data)
        json_data = json_data.replace('"[BODY]"', body.decode())
        headers = self._get_headers()
        url = f"{PAYPAL_API_URL}/v1/notifications/verify-webhook-signature"
        response = httpx.post(url, headers=headers, content=json_data)
        try:
            response.raise_for_status()
        except Exception:
            logger.error(response.text)
            raise
        data = response.json()
        logger.info(data)
        return data["verification_status"] == "SUCCESS"

    async def cancel_subscription(self, subscription_id: str):
        headers = self._get_headers()
        body = {
            # TODO should capture the reason from the user
            "reason": "Requested by user in the app",
        }
        url = f"{PAYPAL_API_URL}/v1/billing/subscriptions/{subscription_id}/cancel"

        async with httpx.AsyncClient() as async_client:
            response = await async_client.post(url, headers=headers, json=body)
            response.raise_for_status()
