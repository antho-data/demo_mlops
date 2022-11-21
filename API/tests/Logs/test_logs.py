from fastapi.testclient import TestClient
from app.routers.login import create_access_token
from app.main import app

def test_usage_logs():

    with TestClient(app) as client:    

        # Admin user

        token = create_access_token("admin", True)
        response = client.get("/usage_logs", headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        assert len(response.content) > 2
        
        # Non admin user 
        
        token = create_access_token("noel", False)
        response = client.get("/usage_logs", headers={'Authorization': f'Bearer {token}'}) 
        assert response.status_code == 401
        assert response.json()["detail"] == 'You are not allowed to perform this operation.'

        # Not existing  user 

        token = create_access_token("lambda_user", False)
        response = client.get("/usage_logs", headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 401
        assert response.json()["detail"] == 'You are not allowed to perform this operation.'

def test_operational_logs():
    
    with TestClient(app) as client:    

        # Admin user    

        token = create_access_token("admin", True)
        response = client.get("/operational_logs", headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        assert len(response.content) > 2

        # Non admin user 
        
        token = create_access_token("noel", False)
        response = client.get("/operational_logs", headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 401
        assert response.json()["detail"] == 'You are not allowed to perform this operation.'

        # Not existing  user 

        token = create_access_token("lambda_user", False)
        response = client.get("/operational_logs", headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 401
        assert response.json()["detail"] == 'You are not allowed to perform this operation.'
