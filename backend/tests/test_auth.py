from tests.conftest import API, register


def test_register_login_me_refresh(client):
    r = register(client)
    assert r.status_code == 201
    body = r.json()
    assert body["user"]["email"] == "asha@example.com"
    assert "password" not in str(body).lower().replace("password_hash", "")  # nothing sensitive echoed

    login = client.post(f"{API}/auth/login", json={"email": "ASHA@example.com", "password": "Passw0rd!x"})
    assert login.status_code == 200
    tokens = login.json()["tokens"]

    me = client.get(f"{API}/auth/me", headers={"Authorization": f"Bearer {tokens['access_token']}"})
    assert me.status_code == 200 and me.json()["full_name"] == "Asha Rao"

    ref = client.post(f"{API}/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert ref.status_code == 200 and ref.json()["access_token"]


def test_duplicate_email_rejected_case_insensitively(client):
    register(client)
    assert register(client, email="Asha@Example.com").status_code == 409


def test_weak_passwords_rejected(client):
    for pw in ["short1", "allletters!", "12345678", "a1" * 40]:
        assert register(client, password=pw).status_code == 422, pw


def test_wrong_password_and_unknown_user_look_identical(client):
    register(client)
    a = client.post(f"{API}/auth/login", json={"email": "asha@example.com", "password": "WrongPass1"})
    b = client.post(f"{API}/auth/login", json={"email": "nobody@example.com", "password": "WrongPass1"})
    assert a.status_code == b.status_code == 401
    assert a.json() == b.json()


def test_protected_routes_require_valid_access_token(client):
    assert client.get(f"{API}/auth/me").status_code == 401
    assert client.get(f"{API}/auth/me", headers={"Authorization": "Bearer garbage"}).status_code == 401


def test_refresh_token_cannot_be_used_as_access_token(client):
    tokens = register(client).json()["tokens"]
    r = client.get(f"{API}/auth/me", headers={"Authorization": f"Bearer {tokens['refresh_token']}"})
    assert r.status_code == 401
    r = client.post(f"{API}/auth/refresh", json={"refresh_token": tokens["access_token"]})
    assert r.status_code == 401
