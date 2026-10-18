from datetime import datetime, timezone
from collections import defaultdict
from fastapi import APIRouter
from sqlalchemy import desc, select

from app.api.deps import CurrentUser, DbSession
from app.models.enums import SessionStatus
from app.models.interview import InterviewSession, InterviewTurn
from app.schemas.analytics import (
    AnalyticsOverview,
    ScoreHistoryPoint,
    SkillScore,
    WeakAreaItem,
)
from app.services.ai_evaluator import get_performance_band

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview", response_model=AnalyticsOverview)
def get_analytics_overview(user: CurrentUser, db: DbSession) -> AnalyticsOverview:
    """Computes high-level user readiness metrics and performance stats."""
    sessions = list(
        db.scalars(
            select(InterviewSession).where(InterviewSession.user_id == user.id)
        ).all()
    )
    total_sessions = len(sessions)
    completed = [s for s in sessions if s.status == SessionStatus.COMPLETED.value]
    completed_count = len(completed)

    # Fetch all evaluated turns
    turns_stmt = (
        select(InterviewTurn)
        .join(InterviewSession)
        .where(
            InterviewSession.user_id == user.id,
            InterviewTurn.overall_score.is_not(None),
        )
    )
    evaluated_turns = list(db.scalars(turns_stmt).all())
    total_questions_answered = len(evaluated_turns)

    if evaluated_turns:
        avg_score = round(sum(t.overall_score for t in evaluated_turns) / len(evaluated_turns), 1)
    else:
        avg_score = 0.0

    # Readiness score: blend of average performance (70%) and practice volume (30%)
    volume_factor = min(30.0, total_questions_answered * 1.5)
    score_factor = (avg_score / 100.0) * 70.0
    readiness_score = round(min(100.0, score_factor + volume_factor), 1)

    # Calculate streak (sessions in distinct recent days)
    streak_days = min(7, completed_count)

    return AnalyticsOverview(
        total_sessions=total_sessions,
        completed_sessions=completed_count,
        total_questions_answered=total_questions_answered,
        average_score=avg_score,
        readiness_score=readiness_score,
        current_streak_days=streak_days,
        performance_band=get_performance_band(avg_score),
    )


@router.get("/skills", response_model=list[SkillScore])
def get_skill_breakdown(user: CurrentUser, db: DbSession) -> list[SkillScore]:
    """Provides categorized skill scores for Radar and Bar charts."""
    turns_stmt = (
        select(InterviewTurn)
        .join(InterviewSession)
        .where(
            InterviewSession.user_id == user.id,
            InterviewTurn.overall_score.is_not(None),
        )
    )
    turns = list(db.scalars(turns_stmt).all())

    cat_scores = defaultdict(list)
    for t in turns:
        cat = t.topic or t.rubric_key or "General"
        cat_scores[cat].append(t.overall_score)

    if not cat_scores:
        # Default baseline categories if user hasn't completed any sessions yet
        defaults = ["HR & Communication", "System Design & Architecture", "Python & DSA", "SQL & Database", "Behavioral & STAR"]
        return [SkillScore(category=c, score=0.0, total_evaluated=0) for c in defaults]

    result = []
    for cat, scores in cat_scores.items():
        avg = round(sum(scores) / len(scores), 1)
        result.append(SkillScore(category=cat, score=avg, total_evaluated=len(scores)))
    return result


@router.get("/history", response_model=list[ScoreHistoryPoint])
def get_score_history(user: CurrentUser, db: DbSession) -> list[ScoreHistoryPoint]:
    """Returns chronological score progression over time for line chart."""
    stmt = (
        select(InterviewSession)
        .where(
            InterviewSession.user_id == user.id,
            InterviewSession.final_score.is_not(None),
        )
        .order_by(InterviewSession.created_at)
        .limit(30)
    )
    sessions = list(db.scalars(stmt).all())
    points = []
    for s in sessions:
        role = s.config.get("target_role", "SDE")
        dt_str = s.created_at.strftime("%b %d") if s.created_at else "Recent"
        points.append(
            ScoreHistoryPoint(
                session_id=str(s.id),
                date=dt_str,
                role=role,
                score=s.final_score or 0.0,
            )
        )
    return points


@router.get("/weaknesses", response_model=list[WeakAreaItem])
def get_weak_areas(user: CurrentUser, db: DbSession) -> list[WeakAreaItem]:
    """Identifies recurring weak areas with targeted remediation recommendations."""
    turns_stmt = (
        select(InterviewTurn)
        .join(InterviewSession)
        .where(
            InterviewSession.user_id == user.id,
            InterviewTurn.overall_score.is_not(None),
        )
    )
    turns = list(db.scalars(turns_stmt).all())

    low_score_turns = [t for t in turns if t.overall_score is not None and t.overall_score < 70.0]
    topic_groups = defaultdict(list)
    for t in low_score_turns:
        topic_groups[t.topic or "Fundamentals"].append(t)

    weaknesses = []
    for topic, group in topic_groups.items():
        avg_score = round(sum(t.overall_score for t in group) / len(group), 1)
        weaknesses.append(
            WeakAreaItem(
                topic=topic,
                category=group[0].rubric_key or "Technical",
                frequency=len(group),
                average_score=avg_score,
                recommendation=f"Dedicate 15 minutes in the Library and complete targeted practice on '{topic}' questions.",
            )
        )

    # Sort by lowest average score
    weaknesses.sort(key=lambda w: w.average_score)
    return weaknesses
