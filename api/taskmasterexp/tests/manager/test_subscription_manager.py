from taskmasterexp.database.managers import SubscriptionManager

SUBSCRIPTION_ID = "I-HBMDL8PL8571"


async def test_activate_subscription(
    test_admin_user, subscription_manager: SubscriptionManager
):
    subscription = await subscription_manager.get_active_subscription(
        test_admin_user.uuid
    )
    assert subscription is None

    subscription = await subscription_manager.link_subscription(
        test_admin_user.uuid, SUBSCRIPTION_ID
    )
    assert subscription.subscription_id == SUBSCRIPTION_ID
    assert subscription.is_active is False

    subscription = await subscription_manager.activate_subscription(
        SUBSCRIPTION_ID, "plan_id"
    )
    assert subscription.is_active is True
    assert subscription.user_id == test_admin_user.uuid

    subscription = await subscription_manager.get_active_subscription(
        test_admin_user.uuid
    )
    assert subscription.subscription_id == SUBSCRIPTION_ID


async def test_race_condition(
    test_admin_user, subscription_manager: SubscriptionManager
):
    subscription = await subscription_manager.get_active_subscription(
        test_admin_user.uuid
    )
    assert subscription is None

    subscription = await subscription_manager.activate_subscription(
        SUBSCRIPTION_ID, "plan_id"
    )
    assert subscription.is_active is True
    assert subscription.user_id is None

    subscription = await subscription_manager.link_subscription(
        test_admin_user.uuid, SUBSCRIPTION_ID
    )
    assert subscription.subscription_id == SUBSCRIPTION_ID
    assert subscription.is_active is True

    subscription = await subscription_manager.get_active_subscription(
        test_admin_user.uuid
    )
    assert subscription.subscription_id == SUBSCRIPTION_ID


async def test_cancel_subscription(
    test_admin_user, subscription_manager: SubscriptionManager
):
    subscription = await subscription_manager.get_active_subscription(
        test_admin_user.uuid
    )
    assert subscription is None

    subscription = await subscription_manager.link_subscription(
        test_admin_user.uuid, SUBSCRIPTION_ID
    )
    assert subscription.subscription_id == SUBSCRIPTION_ID
    assert subscription.is_active is False

    subscription = await subscription_manager.activate_subscription(
        SUBSCRIPTION_ID, "plan_id"
    )
    assert subscription.is_active is True

    subscription = await subscription_manager.get_active_subscription(
        test_admin_user.uuid
    )
    assert subscription.subscription_id == SUBSCRIPTION_ID

    await subscription_manager.cancel_subscription(SUBSCRIPTION_ID)
    subscription = await subscription_manager.get_active_subscription(
        test_admin_user.uuid
    )
    assert subscription is None
