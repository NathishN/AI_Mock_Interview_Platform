from tests.conftest import API, sample_question


def _seed(client, admin_headers, records):
    r = client.post(f"{API}/admin/questions/import", headers=admin_headers, json={"questions": records})
    assert r.status_code == 200, r.text
    return r.json()


def test_library_requires_auth_and_admin_routes_require_admin(client, auth_headers):
    assert client.get(f"{API}/questions").status_code == 401
    r = client.post(f"{API}/admin/questions/import", headers=auth_headers, json={"questions": [sample_question()]})
    assert r.status_code == 403


def test_import_list_filter_search_and_summary(client, admin_headers, auth_headers):
    qs = [
        sample_question(),
        sample_question(
            id="py-001", question="What is the difference between a list and a tuple in Python?",
            category="Python", subcategory="Data Structures", difficulty="Intermediate",
            interview_stage=["Technical"], tags=["python"], target_roles=["Python Developer"],
        ),
    ]
    res = _seed(client, admin_headers, qs)
    assert res["created"] == 2 and res["ok"]

    page = client.get(f"{API}/questions", headers=auth_headers).json()
    assert page["total"] == 2

    assert client.get(f"{API}/questions?category=Python", headers=auth_headers).json()["total"] == 1
    assert client.get(f"{API}/questions?role=Python Developer", headers=auth_headers).json()["total"] == 1
    assert client.get(f"{API}/questions?stage=Final", headers=auth_headers).json()["items"][0]["id"] == "hr-001"
    assert client.get(f"{API}/questions?tag=communication", headers=auth_headers).json()["total"] == 1  # tags lower-cased
    assert client.get(f"{API}/questions?q=TUPLE", headers=auth_headers).json()["total"] == 1
    assert client.get(f"{API}/questions?q=%25", headers=auth_headers).json()["total"] == 0  # LIKE wildcards escaped

    s = client.get(f"{API}/questions/summary", headers=auth_headers).json()
    assert s["total"] == 2 and s["by_category"] == {"HR": 1, "Python": 1}


def test_import_is_atomic_and_reports_every_problem(client, admin_headers, auth_headers):
    good = sample_question()
    dup_id = sample_question(question="A completely different question text here?")
    dup_text = sample_question(id="hr-002", question="tell me about  YOURSELF")
    empty = sample_question(id="hr-003", question="Why should we hire you for this role?", key_points=[" "])
    r = client.post(f"{API}/admin/questions/import", headers=admin_headers,
                    json={"questions": [good, dup_id, dup_text, empty]})
    assert r.status_code == 422
    body = r.json()
    assert body["ok"] is False and {e["index"] for e in body["errors"]} == {1, 2, 3}
    assert client.get(f"{API}/questions", headers=auth_headers).json()["total"] == 0  # nothing was saved


def test_reimport_updates_instead_of_duplicating(client, admin_headers, auth_headers):
    _seed(client, admin_headers, [sample_question()])
    res = _seed(client, admin_headers, [sample_question(difficulty="Advanced")])
    assert res["created"] == 0 and res["updated"] == 1
    assert client.get(f"{API}/questions/hr-001", headers=auth_headers).json()["difficulty"] == "Advanced"


def test_same_text_under_new_id_is_rejected(client, admin_headers):
    _seed(client, admin_headers, [sample_question()])
    r = client.post(f"{API}/admin/questions/import", headers=admin_headers,
                    json={"questions": [sample_question(id="hr-999")]})
    assert r.status_code == 422


def test_default_question_type_follows_category(client, admin_headers, auth_headers):
    _seed(client, admin_headers, [
        sample_question(),
        sample_question(id="code-001", question="Write a function to check whether a string is a palindrome.", category="Coding"),
    ])
    assert client.get(f"{API}/questions/hr-001", headers=auth_headers).json()["question_type"] == "hr"
    assert client.get(f"{API}/questions/code-001", headers=auth_headers).json()["question_type"] == "coding"


def test_admin_update_and_soft_delete(client, admin_headers, auth_headers):
    _seed(client, admin_headers, [sample_question()])
    r = client.put(f"{API}/admin/questions/hr-001", headers=admin_headers, json={"difficulty": "Intermediate", "tags": ["x"]})
    assert r.status_code == 200 and r.json()["difficulty"] == "Intermediate" and r.json()["tags"] == ["x"]

    bad = client.put(f"{API}/admin/questions/hr-001", headers=admin_headers, json={"key_points": []})
    assert bad.status_code == 422

    assert client.delete(f"{API}/admin/questions/hr-001", headers=admin_headers).status_code == 204
    assert client.get(f"{API}/questions/hr-001", headers=auth_headers).status_code == 404
    admin_view = client.get(f"{API}/admin/questions", headers=admin_headers).json()
    assert admin_view["total"] == 1 and admin_view["items"][0]["is_active"] is False

    r = client.put(f"{API}/admin/questions/hr-001", headers=admin_headers, json={"is_active": True})
    assert r.status_code == 200 and r.json()["is_active"] is True
