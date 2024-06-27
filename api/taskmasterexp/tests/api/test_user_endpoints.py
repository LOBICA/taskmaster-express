def test_user_information(test_admin_client, test_admin_user):
    response = test_admin_client.get("/users/me")
    assert response.status_code == 200
    json_data = response.json()
    assert test_admin_user.email == json_data["email"]


def test_register_user(test_client):
    ...


def test_delete_user(test_admin_client, test_admin_user):
    response = test_admin_client.delete("/users/me")
    assert response.status_code == 204

    response = test_admin_client.get("/users/me")
    assert response.status_code == 401
