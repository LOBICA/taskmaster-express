from taskmasterexp.database.managers import SubscriptionManager
from taskmasterexp.paypal.schemas import EventType, WebhookData


async def test_paypal_webhook(test_admin_client):
    data = WebhookData(
        id="WH-1234567890",
        event_type=EventType.SUBSCRIPTION_CREATED,
        resource={
            "id": "I-1234567890",
            "plan_id": "P-1234567890",
            "status": "APPROVAL_PENDING",
        },
    )

    response = test_admin_client.post("/paypal/webhooks/subscription", json=data.dict())
    assert response.status_code == 200


async def test_activate_subscription(
    test_admin_client, subscription_manager: SubscriptionManager
):
    data = WebhookData(
        id="WH-1234567890",
        event_type=EventType.SUBSCRIPTION_ACTIVATED,
        resource={"id": "I-1234567890", "plan_id": "P-1234567890", "status": "ACTIVE"},
    )

    response = test_admin_client.post("/paypal/webhooks/subscription", json=data.dict())
    assert response.status_code == 200

    subscription = await subscription_manager.get_subscription_by_subscription_id(
        "I-1234567890"
    )
    assert subscription is not None
    assert subscription.is_active is True


async def test_cancel_subscription(
    test_admin_client, subscription_manager: SubscriptionManager
):
    subscription = await subscription_manager.activate_subscription(
        "I-1234567890", "P-1234567890"
    )
    assert subscription.is_active is True

    data = WebhookData(
        id="WH-1234567890",
        event_type=EventType.SUBSCRIPTION_CANCELLED,
        resource={
            "id": "I-1234567890",
            "plan_id": "P-1234567890",
            "status": "CANCELLED",
        },
    )

    response = test_admin_client.post("/paypal/webhooks/subscription", json=data.dict())
    assert response.status_code == 200

    subscription = await subscription_manager.get_subscription_by_subscription_id(
        "I-1234567890"
    )
    assert subscription is not None
    assert subscription.is_active is False
