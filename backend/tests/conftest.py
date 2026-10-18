import os

os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-that-is-long-enough-for-hs256")
os.environ["GROQ_API_KEY"] = ""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import User, UserProfile
from app.core.security import hash_password
from app.models.enums import UserRole
from app.scripts.bootstrap import seed_rubrics

API = "/api/v1"


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    with Session() as s:
        seed_rubrics(s)
        yield s
    engine.dispose()


@pytest.fixture()
def client(db_session):
    def _get_db():
        yield db_session

    app.dependency_overrides[get_db] = _get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def register(client, email="asha@example.com", password="Passw0rd!x", name="Asha Rao"):
    return client.post(f"{API}/auth/register", json={"email": email, "password": password, "full_name": name})


@pytest.fixture()
def auth_headers(client):
    tokens = register(client).json()["tokens"]
    return {"Authorization": f"Bearer {tokens['access_token']}"}


@pytest.fixture()
def admin_headers(client, db_session):
    u = User(email="admin@example.com", password_hash=hash_password("Adm1nPass!"), full_name="Admin", role=UserRole.ADMIN.value)
    u.profile = UserProfile()
    db_session.add(u)
    db_session.commit()
    r = client.post(f"{API}/auth/login", json={"email": "admin@example.com", "password": "Adm1nPass!"})
    return {"Authorization": f"Bearer {r.json()['tokens']['access_token']}"}


def sample_question(**overrides):
    q = {
        "id": "hr-001",
        "question": "Tell me about yourself.",
        "category": "HR",
        "subcategory": "Self Introduction",
        "difficulty": "Beginner",
        "target_roles": ["Software Engineer", "AI Engineer"],
        "interview_stage": ["HR", "Final"],
        "reference_answer": "Use present, past, future: current status, relevant skills and projects, then career direction. Keep it under two minutes.",
        "key_points": ["Present status", "Relevant skills"],
        "evaluation_criteria": ["Relevance", "Clarity"],
        "common_mistakes": ["Reciting the resume line by line"],
        "follow_up_questions": ["Which project are you proudest of?"],
        "tags": ["Communication", "fresher"],
    }
    q.update(overrides)
    return q
