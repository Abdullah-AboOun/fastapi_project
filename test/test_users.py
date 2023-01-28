import pytest
from app import schemas
from .database import client, session


def test_root(client):

    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World!'
    assert res.status_code == 200


def test_create_user(client):
    email = "test@gmail.com"
    res = client.post(
        "/users/", json={"email": email, "password": "pass1234"})

    new_user = schemas.UserReturn(**res.json())
    assert new_user.email == email
    assert res.status_code == 201
