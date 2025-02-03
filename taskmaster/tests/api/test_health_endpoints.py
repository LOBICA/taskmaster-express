from taskmaster import __version__


def test_health_endpoints(test_client):
    version_str = f"Taskmaster Express {__version__}"
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.text == version_str

    response = test_client.get("/ping")
    assert response.status_code == 200
    assert response.text == "pong"
