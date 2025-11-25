import jwt
import pytest

from app import schemas, models
from app.config import get_settings
settings = get_settings()
from app.oauth2 import create_access_token



def test_root(client):
    response = client.get("/")
    print(response.json().get("mess"))
    assert response.status_code == 200
    assert response.json() == {"mess": "Welcome to the Posts API!"}

def test_create_user(client):
    response = client.post(
        "/users/", json={"email": "jonnyedwards1@hotmail.co.uk", "password": "password123"})
    
    new_user = schemas.UserResponse(**response.json())
    print(response.json())
    assert new_user.email == "jonnyedwards1@hotmail.co.uk"
    assert response.status_code == 201

def test_login_user(test_user, client):
    response = client.post(
        "/auth/login",
        data={"username": test_user["email"],
              "password": "password123"}
    )
    assert response.status_code == 200

    login_res = schemas.Token(**response.json())
    payload = jwt.decode(
        login_res.access_token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    assert payload["user_id"] == test_user["id"]
    assert login_res.token_type == "bearer"



@pytest.mark.parametrize("email, password, status_code", [
    ("jonnyedwards1@hotmail.co.uk", "wrongpassword", 404),
    ("nonexist@hotmail.co.uk", "password123", 404),
    (None, "password123", 422),
    ("jonnyedwards1@hotmail.co.uk", None, 422)
])
def test_incorrect_login_user(test_user, client, email, password, status_code):

    payload = {}
    if email is not None:
        payload["username"] = email
    if password is not None:
        payload["password"] = password

    response = client.post(
        "/auth/login", data=payload)
    assert response.status_code == status_code

def test_get_all_posts(authorised_client, test_posts):
    resp = authorised_client.get("/posts/")
    print(resp.json())
    assert resp.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    resp = client.get("/posts/")
    print(resp.json())
    assert resp.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    resp = client.get(f"/posts/{test_posts[0].id}")
    assert resp.status_code == 401

def test_get_one_post_not_exist(authorised_client, test_posts):
    resp = authorised_client.get(f"/posts/88888")
    print(resp.json())
    assert resp.status_code == 404

def test_get_one_post(authorised_client, test_posts):
    resp = authorised_client.get(f"/posts/{test_posts[0].id}")
    print(resp.json())
    post = schemas.PostOut(**resp.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content



    



    