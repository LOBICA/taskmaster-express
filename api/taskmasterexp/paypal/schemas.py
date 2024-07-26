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
