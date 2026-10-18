from tests.conftest import API


def test_new_profile_is_empty_and_not_onboarded(client, auth_headers):
    r = client.get(f"{API}/profile/me", headers=auth_headers)
    assert r.status_code == 200
    body = r.json()
    assert body["onboarding_completed"] is False
    assert body["preferred_companies"] == [] and body["full_name"] == "Asha Rao"


def test_partial_updates_and_onboarding_completion(client, auth_headers):
    r = client.put(f"{API}/profile/me", headers=auth_headers, json={"degree": "B.E.", "branch": "CSE (AI & ML)"})
    assert r.json()["onboarding_completed"] is False

    r = client.put(
        f"{API}/profile/me",
        headers=auth_headers,
        json={
            "graduation_year": 2027,
            "target_role": "AI Engineer",
            "preferred_companies": ["Infosys", " Infosys ", "", "TCS"],
            "daily_prep_minutes": 45,
        },
    )
    body = r.json()
    assert body["onboarding_completed"] is True
    assert body["degree"] == "B.E."  # earlier values preserved
    assert body["preferred_companies"] == ["Infosys", "TCS"]  # trimmed + de-duplicated


def test_profile_validation(client, auth_headers):
    for bad in ({"target_role": "Astronaut"}, {"graduation_year": 1980}, {"daily_prep_minutes": 1}):
        assert client.put(f"{API}/profile/me", headers=auth_headers, json=bad).status_code == 422


def test_profiles_are_per_user(client, auth_headers):
    client.put(f"{API}/profile/me", headers=auth_headers, json={"degree": "B.Tech"})
    from tests.conftest import register
    other = register(client, email="ravi@example.com").json()["tokens"]["access_token"]
    r = client.get(f"{API}/profile/me", headers={"Authorization": f"Bearer {other}"})
    assert r.json()["degree"] is None
