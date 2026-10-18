import pytest
from app.services.kb import load_seed
from app.services.question_import import import_questions


@pytest.fixture(autouse=True)
def seed_db(db_session):
    records = load_seed()
    import_questions(db_session, records, update_existing=False)


def test_start_interview_session_creates_first_turn(client, auth_headers):
    resp = client.post(
        "/api/v1/interviews/sessions",
        headers=auth_headers,
        json={
            "target_role": "Software Development Engineer",
            "interview_stage": "Technical",
            "difficulty": "Intermediate",
            "duration_minutes": 30,
            "num_questions": 3,
            "mode": "technical",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "in_progress"
    assert len(data["turns"]) == 1
    t1 = data["turns"][0]
    assert t1["sequence"] == 1
    assert t1["status"] == "asked"
    assert len(t1["question_text"]) > 10


def test_submit_answer_evaluates_and_advances_turn(client, auth_headers):
    # 1. Start session with 2 questions
    create_resp = client.post(
        "/api/v1/interviews/sessions",
        headers=auth_headers,
        json={
            "target_role": "Python Developer",
            "interview_stage": "Technical",
            "difficulty": "Beginner",
            "num_questions": 2,
            "mode": "technical",
        },
    )
    session_id = create_resp.json()["id"]

    # 2. Answer question 1
    ans_resp = client.post(
        f"/api/v1/interviews/sessions/{session_id}/answer",
        headers=auth_headers,
        json={
            "answer_text": "In Python, a list is a mutable dynamic array while a tuple is an immutable sequence. Lists use more memory overhead because they allocate extra capacity for resizing, whereas tuples have fixed memory footprint.",
        },
    )
    assert ans_resp.status_code == 200
    session_data = ans_resp.json()
    turns = session_data["turns"]
    assert len(turns) == 2  # question 1 evaluated + question 2 asked
    t1 = turns[0]
    assert t1["status"] == "evaluated"
    assert t1["overall_score"] is not None
    assert t1["overall_score"] >= 0
    assert "dimension_scores" in t1["evaluation"]
    assert "strengths" in t1["evaluation"]

    # 3. Answer question 2 (reaches target_count of 2)
    ans2_resp = client.post(
        f"/api/v1/interviews/sessions/{session_id}/answer",
        headers=auth_headers,
        json={
            "answer_text": "FastAPI uses Pydantic for request and response validation and Starlette for asynchronous routing. It automatically generates OpenAPI documentation and supports Python type hints.",
        },
    )
    assert ans2_resp.status_code == 200
    final_data = ans2_resp.json()
    assert final_data["status"] == "completed"
    assert final_data["final_score"] is not None
    assert final_data["report"] is not None
    assert "dimension_breakdown" in final_data["report"]


def test_get_session_report(client, auth_headers):
    # Start and finish early
    create_resp = client.post(
        "/api/v1/interviews/sessions",
        headers=auth_headers,
        json={"num_questions": 3},
    )
    session_id = create_resp.json()["id"]

    # Submit 1 answer
    client.post(
        f"/api/v1/interviews/sessions/{session_id}/answer",
        headers=auth_headers,
        json={"answer_text": "Technical concepts require solid understanding of fundamentals and trade-offs."},
    )

    # Get report
    rep_resp = client.get(
        f"/api/v1/interviews/sessions/{session_id}/report",
        headers=auth_headers,
    )
    assert rep_resp.status_code == 200
    rep = rep_resp.json()
    assert rep["session_id"] == session_id
    assert rep["final_score"] >= 0
    assert "performance_band" in rep
    assert len(rep["turns"]) >= 1
