from fastapi.testclient import TestClient
from app.routers.login import create_access_token
from app.main import app
from app.settings import config

client = TestClient(app)


def test_home():
    response = client.get(
        "/", headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert response.json() == {"data":"Hello from API -- Back Office"}

def test_version():
    response = client.get("/version",
                          headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert response.json() == config.get("api_version")

def test_status():
    token = create_access_token("admin", True)
    response = client.get("/status", 
                            headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json() == '1'

    token = create_access_token("lambda_user", False)
    response = client.get("/status",
                          headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 401
    assert response.json()["detail"] == 'You are not allowed to perform this operation.'
