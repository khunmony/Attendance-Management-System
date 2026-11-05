def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_login_and_me(client, admin):
    r = client.post("/api/v1/auth/login", data={"username": "admin@test.local", "password": "secret123"})
    assert r.status_code == 200
    token = r.json()["access_token"]

    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["role"] == "ADMIN"


def test_login_wrong_password(client, admin):
    r = client.post("/api/v1/auth/login", data={"username": "admin@test.local", "password": "nope"})
    assert r.status_code == 401


def test_me_requires_token(client):
    assert client.get("/api/v1/auth/me").status_code == 401
