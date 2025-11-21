from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)

def test_root():
    response = client.get("/")
    print(response.json().get("mess"))
    assert response.status_code == 200
    assert response.json() == {"mess": "Welcome to the Posts API!"}

def test_create_user():
    response = client.post(
        "/users/", json={"email": "jonnyedwards1@hotmail.co.uk", "password": "password123"})
    print(response.json())
    assert response.status_code == 201
    