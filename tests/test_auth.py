import uuid

import pytest
from fastapi.testclient import TestClient

from app.dao.db import get_cursor
from app.main import app

client = TestClient(app)


@pytest.fixture
def username():
    name = f"test_{uuid.uuid4().hex[:8]}"
    yield name
    with get_cursor() as cur:
        cur.execute('DELETE FROM "user" WHERE username = %s', (name,))


def test_first_login_creates_user(username):
    r = client.post("/auth/login", json={"username": username})
    assert r.status_code == 200
    body = r.json()
    assert body["username"] == username
    assert body["created"] is True
    assert body["diet_type"] == "veg"


def test_second_login_reuses_user(username):
    first = client.post("/auth/login", json={"username": username}).json()
    second = client.post("/auth/login", json={"username": username}).json()
    assert second["created"] is False
    assert second["id"] == first["id"]


def test_username_is_normalised(username):
    first = client.post("/auth/login", json={"username": f"  {username.upper()} "}).json()
    assert first["username"] == username


@pytest.mark.parametrize("bad", ["", "ab", "   ", "x" * 51])
def test_invalid_username_rejected(bad):
    r = client.post("/auth/login", json={"username": bad})
    assert r.status_code == 422
