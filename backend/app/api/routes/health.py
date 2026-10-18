from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.api.deps import DbDep

router = APIRouter(tags=["health"])


@router.get("/health")
def liveness() -> dict:
    return {"status": "ok"}


@router.get("/health/ready")
def readiness(db: DbDep) -> dict:
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(503, "Database unavailable")
    return {"status": "ready"}


@router.get("/model-info")
def model_info() -> dict:
    from app.core.config import get_settings
    s = get_settings()
    return {
        "status": "ready",
        "provider": "Groq",
        "model": s.groq_model,
        "configured": bool(s.groq_api_key),
    }

