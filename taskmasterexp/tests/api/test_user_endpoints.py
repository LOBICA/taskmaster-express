from uuid import UUID

from taskmasterexp.database.managers import UserManager
from taskmasterexp.database.models import UserModel


def test_user_information(test_admin_client, test_admin_user):
    response = test_admin_client.get("/users/me")
    assert response.status_code == 200
    json_data = response.json()
    assert test_admin_user.email == json_data["email"]


async def test_register_user(test_client, user_manager: UserManager):
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "test-password",
    }

    response = test_client.post("/users", json=user_data)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["email"] == user_data["email"]

    user = await user_manager.get(UUID(json_data["uuid"]))
    assert user is not None
    assert user.email == user_data["email"]


async def test_change_password(
    test_admin_client, admin_user_password, test_admin_user, db_session
):
    user: UserModel = await db_session.get(UserModel, test_admin_user.uuid)
    assert user.verify_password(admin_user_password)

    new_password = "654321"
    response = test_admin_client.post(
        "/users/me/password",
        json={
            "password": admin_user_password,
            "newPassword": new_password,
        },
    )
    assert response.status_code == 204

    await db_session.refresh(user)
    assert user.verify_password(admin_user_password) is False
    assert user.verify_password(new_password)

    new_password = "654321"
    response = test_admin_client.post(
        "/users/me/password",
        json={
            "password": admin_user_password,
            "newPassword": new_password,
        },
    )
    assert response.status_code == 401


async def test_delete_user(
    test_admin_client, test_admin_user, user_manager: UserManager
):
    response = test_admin_client.delete("/users/me")
    assert response.status_code == 204

    response = test_admin_client.get("/users/me")
    assert response.status_code == 401

    user = await user_manager.get(test_admin_user.uuid)
    assert user is None
