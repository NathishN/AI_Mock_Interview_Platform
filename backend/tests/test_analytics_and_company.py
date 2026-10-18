def test_analytics_overview_and_skills(client, auth_headers):
    # Overview
    resp = client.get("/api/v1/analytics/overview", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "readiness_score" in data
    assert "average_score" in data
    assert "total_sessions" in data

    # Skills
    skills_resp = client.get("/api/v1/analytics/skills", headers=auth_headers)
    assert skills_resp.status_code == 200
    skills = skills_resp.json()
    assert len(skills) >= 3


def test_company_prep_endpoints(client, auth_headers):
    # List companies
    list_resp = client.get("/api/v1/company-prep", headers=auth_headers)
    assert list_resp.status_code == 200
    comps = list_resp.json()
    assert len(comps) >= 4
    slugs = [c["slug"] for c in comps]
    assert "tcs" in slugs
    assert "amazon" in slugs

    # Detail
    tcs_resp = client.get("/api/v1/company-prep/tcs", headers=auth_headers)
    assert tcs_resp.status_code == 200
    tcs = tcs_resp.json()
    assert tcs["name"] == "Tata Consultancy Services"
    assert len(tcs["rounds"]) >= 3


def test_learning_roadmap(client, auth_headers):
    resp = client.get("/api/v1/roadmap", headers=auth_headers)
    assert resp.status_code == 200
    roadmap = resp.json()
    assert roadmap["total_weeks"] >= 4
    assert len(roadmap["milestones"]) >= 4
