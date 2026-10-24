import io
from tests.conftest import API


SAMPLE_RESUME_TEXT = """
Priya Sharma
Email: priya@example.com | Phone: +91 9876543210
Education: B.Tech in Computer Science, IIT Bombay, 2025 (GPA: 8.9)

Technical Skills:
- Languages: Python, JavaScript, TypeScript, SQL
- Frameworks: FastAPI, React, Node.js, Express
- Databases: PostgreSQL, Redis
- Tools: Docker, Git, Postman, Linux

Projects:
1. Distributed E-Commerce Microservice (Python, FastAPI, PostgreSQL, Redis)
   - Built an asynchronous order management system handling 10,000 requests per minute.
   - Reduced database latency by 45% using Redis caching and connection pooling.
   - Deployed containerized services with Docker.

2. Real-Time Chat & Collab Platform (React, WebSocket, Node.js)
   - Developed end-to-end encrypted messaging with typing indicators and status broadcast.
"""


def test_resume_upload_text_and_fetch_latest(client, auth_headers):
    # Upload text
    resp = client.post(
        f"{API}/resumes/upload-text",
        headers=auth_headers,
        json={
            "raw_text": SAMPLE_RESUME_TEXT,
            "filename": "priya_resume.txt",
            "target_role": "Software Development Engineer",
        },
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["filename"] == "priya_resume.txt"
    assert "analysis" in data
    assert data["analysis"]["ats_score"] > 50
    assert len(data["analysis"]["generated_questions"]) >= 3
    resume_id = data["id"]

    # Verify latest
    latest_resp = client.get(f"{API}/resumes/latest", headers=auth_headers)
    assert latest_resp.status_code == 200
    assert latest_resp.json()["id"] == resume_id

    # Verify list
    list_resp = client.get(f"{API}/resumes", headers=auth_headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1


def test_resume_upload_file(client, auth_headers):
    file_bytes = SAMPLE_RESUME_TEXT.encode("utf-8")
    files = {"file": ("priya_resume.txt", io.BytesIO(file_bytes), "text/plain")}
    data = {"target_role": "Full Stack Developer"}

    resp = client.post(
        f"{API}/resumes/upload",
        headers=auth_headers,
        files=files,
        data=data,
    )
    assert resp.status_code == 201, resp.text
    result = resp.json()
    assert result["filename"] == "priya_resume.txt"
    assert len(result["analysis"]["generated_questions"]) >= 3


def test_start_resume_interview_and_answer(client, auth_headers):
    # 1. Upload resume
    resp = client.post(
        f"{API}/resumes/upload-text",
        headers=auth_headers,
        json={
            "raw_text": SAMPLE_RESUME_TEXT,
            "filename": "priya_resume.txt",
            "target_role": "Software Development Engineer",
        },
    )
    assert resp.status_code == 201
    resume_id = resp.json()["id"]

    # 2. Start interview directly from resume
    session_resp = client.post(
        f"{API}/resumes/{resume_id}/start-interview",
        headers=auth_headers,
        json={"num_questions": 3, "company": "Amazon"},
    )
    assert session_resp.status_code == 201, session_resp.text
    session_data = session_resp.json()
    session_id = session_data["id"]
    assert session_data["status"] == "in_progress"
    assert session_data["config"]["mode"] == "resume"
    assert len(session_data["turns"]) == 1

    first_turn = session_data["turns"][0]
    assert first_turn["status"] == "asked"
    assert len(first_turn["question_text"]) > 10

    # 3. Answer Turn 1
    answer_resp = client.post(
        f"{API}/interviews/sessions/{session_id}/answer",
        headers=auth_headers,
        json={
            "answer_text": "In the Distributed E-Commerce Microservice, I separated read and write traffic, configured Redis as a look-aside cache with a 15-minute TTL, and implemented PostgreSQL write-ahead logging to guarantee ACID compliance."
        },
    )
    assert answer_resp.status_code == 200, answer_resp.text
    updated_session = answer_resp.json()
    assert updated_session["turns"][0]["status"] == "evaluated"
    assert updated_session["turns"][0]["overall_score"] is not None
    assert len(updated_session["turns"]) >= 2


def test_evaluate_resume_question_in_place(client, auth_headers):
    # 1. Upload resume
    resp = client.post(
        f"{API}/resumes/upload-text",
        headers=auth_headers,
        json={
            "raw_text": SAMPLE_RESUME_TEXT,
            "filename": "priya_resume.txt",
            "target_role": "Software Development Engineer",
        },
    )
    assert resp.status_code == 201
    resume_data = resp.json()
    resume_id = resume_data["id"]
    q1 = resume_data["analysis"]["generated_questions"][0]

    # 2. Evaluate individual question
    eval_resp = client.post(
        f"{API}/resumes/{resume_id}/evaluate-question",
        headers=auth_headers,
        json={
            "question_id": q1["id"],
            "question_text": q1["question"],
            "answer_text": "I used Python and FastAPI with Redis caching to handle 2000 requests per minute with p99 latency under 45ms.",
            "target_role": "Software Development Engineer",
            "rubric_key": "technical",
        },
    )
    assert eval_resp.status_code == 200, eval_resp.text
    result = eval_resp.json()
    assert "overall_score" in result
    assert result["overall_score"] >= 0
    assert "feedback" in result or "strengths" in result
