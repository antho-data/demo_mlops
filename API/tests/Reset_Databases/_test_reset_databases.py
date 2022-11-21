from fastapi.testclient import TestClient
from app.routers.login import create_access_token
from app.main import app

# Not usable because database will be reset to production mode instead of test mode 

def test_reset_databases():
    with TestClient(app) as client:    

        # Admin user 

        token = create_access_token("admin", True)
        response = client.get("/reset_databases", headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        assert len(response.content) >= 1


        # Non admin user 
        
        token = create_access_token("noel", False)
        response = client.get("/reset_databases", headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 401
        assert response.json()["detail"] == 'You are not allowed to perform this operation.'

        # Not existing  user 

        token = create_access_token("lambda_user", False)
        response = client.get("/reset_databases", headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 401
        assert response.json()["detail"] == 'You are not allowed to perform this operation.'
