from app.routers.login import create_access_token
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

"""

def test_user():

    # user n'ayant pas les droits d'accès à la table api_users : inactive
    user_not_access_token = create_access_token({"sub": "not_admin"})
    response = client.get("/user/", headers={'Authorization': f'Bearer {user_not_access_token}'})
    assert response.status_code == 404
    assert response.json()["detail"] == 'inactive user'


    user_access_token = create_access_token({"sub": "admin@d-aim.com"})
    # voir tous les users
    response = client.get("/user/", headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 200
    assert len(response.json()) == 2


    # voir un seul user
    response = client.get("/user/2", headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 200
    assert len(response.json()) == 4

    # créer un seul user
    response = client.post("/user/", headers={'Authorization': f'Bearer {user_access_token}'}, json= {"login": "admin_test@d-aim.com", "password": "0000", "is_admin": False})
    assert response.status_code == 200


    # modifier un user
    response = client.put("/user/3", headers={'Authorization': f'Bearer {user_access_token}'}, json={"is_admin": "true"})
    assert response.status_code == 200

    # supprimer un user
    response = client.delete("/user/3", headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 200


    # mauvais token
    response = client.get("/user/", headers={'Authorization': f'Bearer bsljgrokirzoknnkjrnvbzlncflkjb'})
    assert response.status_code == 401
    assert response.json()['detail'] == "Couldn't validate credentials"


"""


