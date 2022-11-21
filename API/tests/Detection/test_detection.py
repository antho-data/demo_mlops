from fastapi.testclient import TestClient
from app.routers.login import create_access_token
from app.main import app
import os


def test_detection():
    with TestClient(app) as client:
        token = create_access_token("admin", True)
        filepath = "./tests/detection/test_pic002.jpg"
        response = client.post("/detection",
                              headers={'Authorization': f'Bearer {token}'},
                              files={"file": (os.path.basename(filepath), open(filepath, "rb"), "image/jpeg")})

        assert response.status_code == 200
        assert len(response.content) >= os.path.getsize(filepath)


        token = create_access_token("lambda_user", False)
        filepath = "./tests/detection/test_pic001.jpg"
        response = client.post("/detection",
                              headers = {'Authorization': f'Bearer {token}'},
                              files={"file": (os.path.basename(filepath), open(filepath, "rb"), "image/jpeg")})

        assert response.status_code == 401
        assert response.json()["detail"] == 'You are not allowed to perform this operation.'
