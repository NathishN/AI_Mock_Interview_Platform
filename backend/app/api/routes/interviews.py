import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, DbSession
from app.models.enums import SessionStatus, TurnStatus
from app.models.interview import InterviewSession, InterviewTurn
from app.schemas.interview import (
    AnswerSubmitIn,
    InterviewSessionCreate,
    InterviewSessionDetail,
    InterviewSessionSummary,
    InterviewTurnOut,
    ReportOut,
)
from app.services.interview_flow import (
    conclude_interview_session,
    process_candidate_answer,
    start_interview_session,
)

router = APIRouter(prefix="/interviews", tags=["interviews"])


@router.post("/sessions", response_model=InterviewSessionDetail, status_code=status.HTTP_201_CREATED)
def create_session(
    body: InterviewSessionCreate,
    user: CurrentUser,
    db: DbSession,
) -> InterviewSession:
    """Start a new realistic mock interview session."""
    session = start_interview_session(
        db=db,
        user_id=user.id,
        config=body.model_dump(),
    )
    return session


@router.get("/sessions", response_model=list[InterviewSessionSummary])
def list_user_sessions(
    user: CurrentUser,
    db: DbSession,
    limit: int = 20,
) -> list[InterviewSession]:
    """Retrieve history of user's mock interview sessions."""
    stmt = (
        select(InterviewSession)
        .where(InterviewSession.user_id == user.id)
        .order_by(desc(InterviewSession.created_at))
        .limit(limit)
    )
    return list(db.scalars(stmt).all())


@router.get("/sessions/{session_id}", response_model=InterviewSessionDetail)
def get_session_detail(
    session_id: uuid.UUID,
    user: CurrentUser,
    db: DbSession,
) -> InterviewSession:
    """Fetch session details and turns. State is persistent so page refreshes don't lose progress."""
    session = db.get(InterviewSession, session_id)
    if not session or session.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")
    return session


@router.post("/sessions/{session_id}/answer", response_model=InterviewSessionDetail)
def submit_answer(
    session_id: uuid.UUID,
    body: AnswerSubmitIn,
    user: CurrentUser,
    db: DbSession,
) -> InterviewSession:
    """Submit answer for the current pending question and trigger AI evaluation."""
    session = db.get(InterviewSession, session_id)
    if not session or session.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")

    if session.status != SessionStatus.IN_PROGRESS.value:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Interview session is not active")

    # Find the current asked turn
    asked_turn = next((t for t in session.turns if t.status == TurnStatus.ASKED.value), None)
    if not asked_turn:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No pending question to answer")

    process_candidate_answer(
        db=db,
        session=session,
        turn=asked_turn,
        answer_text=body.answer_text,
    )
    return session


@router.post("/sessions/{session_id}/retry-eval/{turn_id}", response_model=InterviewTurnOut)
def retry_turn_evaluation(
    session_id: uuid.UUID,
    turn_id: uuid.UUID,
    user: CurrentUser,
    db: DbSession,
) -> InterviewTurn:
    """Retries evaluation for a specific turn if AI evaluation previously failed."""
    session = db.get(InterviewSession, session_id)
    if not session or session.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")

    turn = db.get(InterviewTurn, turn_id)
    if not turn or turn.session_id != session.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview turn not found")

    if not turn.answer_text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Turn has no submitted answer to evaluate")

    process_candidate_answer(
        db=db,
        session=session,
        turn=turn,
        answer_text=turn.answer_text,
    )
    return turn


@router.post("/sessions/{session_id}/finish", response_model=InterviewSessionDetail)
def finish_session_early(
    session_id: uuid.UUID,
    user: CurrentUser,
    db: DbSession,
) -> InterviewSession:
    """Concludes the interview session early and generates the final performance report."""
    session = db.get(InterviewSession, session_id)
    if not session or session.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")

    conclude_interview_session(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("/sessions/{session_id}/report", response_model=ReportOut)
def get_session_report(
    session_id: uuid.UUID,
    user: CurrentUser,
    db: DbSession,
) -> ReportOut:
    """Fetches the comprehensive performance report and dimension scores for a completed session."""
    session = db.get(InterviewSession, session_id)
    if not session or session.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")

    if session.status != SessionStatus.COMPLETED.value:
        conclude_interview_session(session)
        db.commit()
        db.refresh(session)

    rep = session.report or {}
    return ReportOut(
        session_id=session.id,
        status=session.status,
        final_score=session.final_score or 0.0,
        performance_band=rep.get("performance_band", "Requires additional practice"),
        total_questions=rep.get("total_questions", len(session.turns)),
        dimension_breakdown=rep.get("dimension_breakdown", []),
        strengths=rep.get("strengths", []),
        areas_for_improvement=rep.get("areas_for_improvement", []),
        practice_recommendations=rep.get("practice_recommendations", []),
        turns=session.turns,
    )
