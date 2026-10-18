import re
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import String, cast, func, or_, select
from sqlalchemy.dialects.postgresql import JSONB

from app.api.deps import CurrentUser, DbDep
from app.models import Question
from app.models.enums import Difficulty, QuestionCategory
from app.schemas.question import QuestionOut, QuestionPage, QuestionSummary

router = APIRouter(prefix="/questions", tags=["questions"])


def json_list_contains(db, column, value: str):
    """Portable 'JSON array contains value' for PostgreSQL (JSONB) and SQLite (tests)."""
    if db.get_bind().dialect.name == "postgresql":
        return cast(column, JSONB).contains([value])
    return cast(column, String).like(f'%"{value}"%')


def _escape_like(s: str) -> str:
    return re.sub(r"([%_\\])", r"\\\1", s)


def build_filters(
    db, *, category, difficulty, role, stage, tag, q, include_inactive: bool = False
):
    conds = []
    if not include_inactive:
        conds.append(Question.is_active.is_(True))
    if category:
        conds.append(Question.category == category.value)
    if difficulty:
        conds.append(Question.difficulty == difficulty.value)
    if role:
        conds.append(json_list_contains(db, Question.target_roles, role))
    if stage:
        conds.append(json_list_contains(db, Question.interview_stage, stage))
    if tag:
        conds.append(json_list_contains(db, Question.tags, tag.lower()))
    if q:
        like = f"%{_escape_like(q.strip().lower())}%"
        conds.append(
            or_(
                func.lower(Question.question).like(like, escape="\\"),
                func.lower(Question.subcategory).like(like, escape="\\"),
            )
        )
    return conds


@router.get("", response_model=QuestionPage)
def list_questions(
    db: DbDep,
    _user: CurrentUser,
    category: QuestionCategory | None = None,
    difficulty: Difficulty | None = None,
    role: Annotated[str | None, Query(max_length=80)] = None,
    stage: Annotated[str | None, Query(max_length=40)] = None,
    tag: Annotated[str | None, Query(max_length=40)] = None,
    q: Annotated[str | None, Query(max_length=100)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> QuestionPage:
    conds = build_filters(db, category=category, difficulty=difficulty, role=role, stage=stage, tag=tag, q=q)
    total = db.scalar(select(func.count()).select_from(Question).where(*conds)) or 0
    items = db.scalars(
        select(Question).where(*conds).order_by(Question.id).offset((page - 1) * page_size).limit(page_size)
    ).all()
    return QuestionPage(items=items, total=total, page=page, page_size=page_size)


@router.get("/summary", response_model=QuestionSummary)
def summary(db: DbDep, _user: CurrentUser) -> QuestionSummary:
    active = Question.is_active.is_(True)
    by_cat = dict(db.execute(select(Question.category, func.count()).where(active).group_by(Question.category)).all())
    by_diff = dict(db.execute(select(Question.difficulty, func.count()).where(active).group_by(Question.difficulty)).all())
    return QuestionSummary(total=sum(by_cat.values()), by_category=by_cat, by_difficulty=by_diff)


@router.get("/{question_id}", response_model=QuestionOut)
def get_question(question_id: str, db: DbDep, _user: CurrentUser) -> Question:
    row = db.get(Question, question_id)
    if row is None or not row.is_active:
        raise HTTPException(404, "Question not found")
    return row
