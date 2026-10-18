def test_get_hr_topics(client, auth_headers):
    resp = client.get("/api/v1/hr-studio/topics", headers=auth_headers)
    assert resp.status_code == 200
    topics = resp.json()
    assert len(topics) >= 5
    ids = [t["id"] for t in topics]
    assert "self_introduction" in ids
    assert "weakness" in ids


def test_generate_hr_answer_from_facts(client, auth_headers):
    resp = client.post(
        "/api/v1/hr-studio/generate",
        headers=auth_headers,
        json={
            "topic": "self_introduction",
            "facts": {
                "degree_and_college": "B.Tech in Computer Science from Anna University",
                "key_skills": "Python, PostgreSQL, and Data Structures",
                "flagship_project": "Smart Interview Prep SaaS with Groq LLM",
                "soft_strengths": "analytical thinking and persistence",
                "career_goal": "deliver high impact as a Software Development Engineer",
            },
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["topic"] == "self_introduction"
    assert "Anna University" in data["generated_answer"]
    assert "Smart Interview Prep" in data["generated_answer"]


def test_analyze_hr_answer(client, auth_headers):
    resp = client.post(
        "/api/v1/hr-studio/analyze",
        headers=auth_headers,
        json={
            "topic": "weakness",
            "answer_text": "I am a total perfectionist and workaholic. I work 16 hours a day and never rest.",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["score"] < 70
    assert any("perfectionist" in p.lower() or "workaholic" in p.lower() for p in data["vague_phrases"])


def test_save_and_retrieve_hr_draft(client, auth_headers):
    save_resp = client.post(
        "/api/v1/hr-studio/drafts",
        headers=auth_headers,
        json={
            "topic": "self_introduction",
            "facts": {"college": "IIT Madras"},
            "final_answer": "My finalized self introduction answer text ready for interview day.",
        },
    )
    assert save_resp.status_code == 201
    draft_id = save_resp.json()["id"]

    list_resp = client.get("/api/v1/hr-studio/drafts", headers=auth_headers)
    assert list_resp.status_code == 200
    drafts = list_resp.json()
    assert any(d["id"] == draft_id for d in drafts)
