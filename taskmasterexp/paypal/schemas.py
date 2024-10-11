from enum import Enum

from pydantic import BaseModel


class Product(BaseModel):
    id_: str
    name: str
    description: str


class FrequencyData(BaseModel):
    interval_unit: str
    interval_count: int


class PriceData(BaseModel):
    currency_code: str
    value: str


class PricingSchemeData(BaseModel):
    fixed_price: PriceData


class BillingCycleData(BaseModel):
    frequency: FrequencyData
    tenure_type: str
    sequence: int
    total_cycles: int
    pricing_scheme: PricingSchemeData | None = None


class PaymentPreferencesData(BaseModel):
    auto_bill_outstanding: bool
    payment_failure_threshold: int


class SubscriptionPlanData(BaseModel):
    product_id: str
    name: str
    description: str
    billing_cycles: list[BillingCycleData] = []
    payment_preferences: PaymentPreferencesData | None = None


class SubscriptionPlan(SubscriptionPlanData):
    id_: str
    status: str


class EventType(str, Enum):
    SUBSCRIPTION_CREATED = "BILLING.SUBSCRIPTION.CREATED"
    SUBSCRIPTION_ACTIVATED = "BILLING.SUBSCRIPTION.ACTIVATED"
    SUBSCRIPTION_UPDATED = "BILLING.SUBSCRIPTION.UPDATED"
    SUBSCRIPTION_EXPIRED = "BILLING.SUBSCRIPTION.EXPIRED"
    SUBSCRIPTION_CANCELLED = "BILLING.SUBSCRIPTION.CANCELLED"
    SUBSCRIPTION_SUSPENDED = "BILLING.SUBSCRIPTION.SUSPENDED"


class WebhookData(BaseModel):
    id: str
    event_type: str
    resource: "WebhookResource"


class WebhookResource(BaseModel):
    id: str
    plan_id: str
    status: str


WebhookData.model_rebuild()
