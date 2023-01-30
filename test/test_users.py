import pytest
from app import schemas
from jose import jwt
from app.config import settings


def test_root(client):

    res = client.get("/")
    assert res.json().get('message') == 'Hello World!'
    assert res.status_code == 200


def test_create_user(client):
    email = "test1@gmail.com"
    res = client.post(
        "/users/", json={"email": email, "password": "pass1234"})

    new_user = schemas.UserReturn(**res.json())
    assert new_user.email == email
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])

    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "pass1234", 403),
    ("test@gmail.com", "wrong password", 403),
    ("wrongemail@gmail.com", "wrong password", 403),
    (None, "wrong password", 422),
    ("test@gmail.com", None, 422),
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password":  password})
    assert res.status_code == status_code
