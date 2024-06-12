from datetime import timedelta

import jwt

from taskmasterexp.auth.token import Token, create_access_token, create_refresh_token
from taskmasterexp.settings import ALGORITHM, SECRET_KEY


def test_login(test_client, test_admin_user, admin_user_password):
    response = test_client.post(
        "/token",
        content=f"username={test_admin_user.email}&password={admin_user_password}",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    assert response.status_code == 200
    json_data = response.json()
    access_token = json_data["access_token"]

    response = test_client.get(
        "/users/me",
        headers={
            "authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200


def test_access_token(test_client, test_admin_user):
    access_token = create_access_token(Token.create_with_username(test_admin_user.uuid))

    response = test_client.get(
        "/users/me",
        headers={
            "authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["uuid"] == str(test_admin_user.uuid)


def test_refresh_token(test_client, test_admin_user, admin_user_password):
    response = test_client.post(
        "/token",
        content=f"username={test_admin_user.email}&password={admin_user_password}",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    assert response.status_code == 200
    json_data = response.json()
    access_token = json_data["access_token"]
    refresh_token = json_data["refresh_token"]
    assert refresh_token

    decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["fresh"] is True

    response = test_client.get(
        "/users/me",
        headers={
            "authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200

    response = test_client.post(
        "/refresh",
        json={
            "refreshToken": refresh_token,
        },
    )
    assert response.status_code == 200
    json_data = response.json()
    new_access_token = json_data["access_token"]
    assert new_access_token != access_token
    decoded_token = jwt.decode(new_access_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["fresh"] is False

    response = test_client.get(
        "/users/me",
        headers={
            "authorization": f"Bearer {new_access_token}",
        },
    )
    assert response.status_code == 200


def test_access_token_cannot_refresh(test_client, test_admin_user, admin_user_password):
    response = test_client.post(
        "/token",
        content=f"username={test_admin_user.email}&password={admin_user_password}",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    assert response.status_code == 200
    json_data = response.json()
    access_token = json_data["access_token"]

    response = test_client.post(
        "/refresh",
        json={
            "refreshToken": access_token,
        },
    )
    assert response.status_code == 401


def test_expired_token(test_client, test_admin_user):
    expire_delta = timedelta(minutes=-15)
    access_token = create_access_token(
        Token.create_with_username(test_admin_user.uuid),
        expires_delta=expire_delta,
    )

    response = test_client.get(
        "/users/me",
        headers={
            "authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 401


def test_expired_refresh_token(test_client, test_admin_user):
    expire_delta = timedelta(minutes=-15)
    refresh_token = create_refresh_token(
        Token.create_with_username(test_admin_user.uuid),
        expires_delta=expire_delta,
    )

    response = test_client.post(
        "/refresh",
        json={
            "refreshToken": refresh_token,
        },
    )
    assert response.status_code == 401
