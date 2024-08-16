from taskmasterexp.database.managers import SubscriptionManager

ORDER_ID = "I-HBMDL8PL8571"


async def test_activate_subscription(
    test_admin_user, subscription_manager: SubscriptionManager
):
    subscription = await subscription_manager.get_active_subscription(
        test_admin_user.uuid
    )
    assert subscription is None

    subscription = await subscription_manager.add_subscription(
        test_admin_user.uuid, ORDER_ID
    )
    assert subscription.order_id == ORDER_ID
    assert subscription.is_active == False

    subscription = await subscription_manager.activate_subscription(ORDER_ID, "plan_id")
    assert subscription.is_active == True
    assert subscription.user_id == test_admin_user.uuid

    subscription = await subscription_manager.get_active_subscription(
        test_admin_user.uuid
    )
    assert subscription.order_id == ORDER_ID


async def test_race_condition(
    test_admin_user, subscription_manager: SubscriptionManager
):
    subscription = await subscription_manager.get_active_subscription(
        test_admin_user.uuid
    )
    assert subscription is None

    subscription = await subscription_manager.activate_subscription(ORDER_ID, "plan_id")
    assert subscription.is_active == True
    assert subscription.user_id is None

    subscription = await subscription_manager.add_subscription(
        test_admin_user.uuid, ORDER_ID
    )
    assert subscription.order_id == ORDER_ID
    assert subscription.is_active == True

    subscription = await subscription_manager.get_active_subscription(
        test_admin_user.uuid
    )
    assert subscription.order_id == ORDER_ID


async def test_cancel_subscription(
    test_admin_user, subscription_manager: SubscriptionManager
):
    subscription = await subscription_manager.get_active_subscription(
        test_admin_user.uuid
    )
    assert subscription is None

    subscription = await subscription_manager.add_subscription(
        test_admin_user.uuid, ORDER_ID
    )
    assert subscription.order_id == ORDER_ID
    assert subscription.is_active == False

    subscription = await subscription_manager.activate_subscription(ORDER_ID, "plan_id")
    assert subscription.is_active == True

    subscription = await subscription_manager.get_active_subscription(
        test_admin_user.uuid
    )
    assert subscription.order_id == ORDER_ID

    await subscription_manager.cancel_subscription(ORDER_ID)
    subscription = await subscription_manager.get_active_subscription(
        test_admin_user.uuid
    )
    assert subscription is None
