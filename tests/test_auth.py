import jwt
import pytest

from app import schemas
from app.config import get_settings
settings = get_settings()


def test_login_correct(test_user, client):
    response = client.post(
        "/auth/login",
        data={"username": test_user["email"], "password": "password123"}
    )

    assert response.status_code == 200

    token = schemas.Token(**response.json())
    payload = jwt.decode(
        token.access_token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    assert payload["user_id"] == test_user["id"]


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


def test_login_incorrect_password(test_user, client):
    r = client.post("/auth/login", data={"username": test_user["email"], "password": "wrong"})
    assert r.status_code == 404


def test_login_user_not_exist(client):
    r = client.post("/auth/login", data={"username": "noone@example.com", "password": "password123"})
    assert r.status_code == 404


def test_login_missing_fields(client):
    r = client.post("/auth/login", data={"username": test_user["email"]})
    assert r.status_code == 422
