from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get(
        "/", headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Welcome to Object detection" in response.content
    response = client.get("/static/css/style3.css")
    assert response.status_code == 200


def test_page_about():
    response = client.get("/page/about",
                          headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"About" in response.content

def test_login():
    response = client.get("/login",
                          headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Login" in response.content

def test_unsplash():
    response = client.get("/detection",
                          headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Object detection" in response.content
