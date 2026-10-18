from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response, status
from sqlalchemy import func, select

from app.api.deps import AdminUser, DbDep
from app.api.routes.questions import build_filters
from app.models import Question, Rubric, question_fingerprint
from app.models.enums import Difficulty, QuestionCategory
from app.schemas.question import (
    ImportRequest,
    ImportResult,
    QuestionCreate,
    QuestionOut,
    QuestionPage,
    QuestionUpdate,
)
from app.schemas.rubric import RubricIn, RubricOut
from app.services.question_import import import_questions

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/questions", response_model=QuestionPage)
def admin_list(
    db: DbDep,
    _admin: AdminUser,
    category: QuestionCategory | None = None,
    difficulty: Difficulty | None = None,
    q: Annotated[str | None, Query(max_length=100)] = None,
    include_inactive: bool = True,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 25,
) -> QuestionPage:
    conds = build_filters(
        db, category=category, difficulty=difficulty, role=None, stage=None, tag=None, q=q,
        include_inactive=include_inactive,
    )
    total = db.scalar(select(func.count()).select_from(Question).where(*conds)) or 0
    items = db.scalars(
        select(Question).where(*conds).order_by(Question.id).offset((page - 1) * page_size).limit(page_size)
    ).all()
    return QuestionPage(items=items, total=total, page=page, page_size=page_size)


@router.post("/questions", response_model=ImportResult, status_code=status.HTTP_201_CREATED)
def create_question(body: QuestionCreate, db: DbDep, _admin: AdminUser, response: Response) -> ImportResult:
    if db.get(Question, body.id):
        raise HTTPException(status.HTTP_409_CONFLICT, f"Question id '{body.id}' already exists")
    result = import_questions(db, [body.model_dump(mode="json")])
    if not result.ok:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return result


@router.put("/questions/{question_id}", response_model=QuestionOut)
def update_question(question_id: str, body: QuestionUpdate, db: DbDep, _admin: AdminUser) -> Question:
    row = db.get(Question, question_id)
    if row is None:
        raise HTTPException(404, "Question not found")
    changes = body.model_dump(exclude_unset=True, mode="json")
    is_active = changes.pop("is_active", None)
    if changes:
        merged = {
            "id": row.id, "question": row.question, "category": row.category,
            "subcategory": row.subcategory, "difficulty": row.difficulty,
            "question_type": row.question_type, "target_roles": row.target_roles,
            "interview_stage": row.interview_stage, "reference_answer": row.reference_answer,
            "key_points": row.key_points, "evaluation_criteria": row.evaluation_criteria,
            "common_mistakes": row.common_mistakes, "follow_up_questions": row.follow_up_questions,
            "tags": row.tags, "rubric_key": row.rubric_key,
        }
        merged.update(changes)
        if "category" in changes and "question_type" not in changes:
            merged["question_type"] = None  # re-derive from the new category
        result = import_questions(db, [merged])
        if not result.ok:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, [e.model_dump() for e in result.errors])
        db.refresh(row)
    if is_active is not None:
        row.is_active = is_active
        db.commit()
    return row


@router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_question(question_id: str, db: DbDep, _admin: AdminUser) -> None:
    """Soft delete: past interviews keep referencing the question."""
    row = db.get(Question, question_id)
    if row is None:
        raise HTTPException(404, "Question not found")
    row.is_active = False
    db.commit()


@router.post("/questions/import", response_model=ImportResult)
def bulk_import(body: ImportRequest, db: DbDep, _admin: AdminUser, response: Response) -> ImportResult:
    result = import_questions(db, body.questions)
    if not result.ok:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return result


@router.get("/rubrics", response_model=list[RubricOut])
def list_rubrics(db: DbDep, _admin: AdminUser) -> list[Rubric]:
    return list(db.scalars(select(Rubric).order_by(Rubric.key)))


@router.put("/rubrics/{key}", response_model=RubricOut)
def upsert_rubric(key: str, body: RubricIn, db: DbDep, _admin: AdminUser) -> Rubric:
    if not key.replace("_", "").replace("-", "").isalnum() or len(key) > 40:
        raise HTTPException(422, "Invalid rubric key")
    row = db.get(Rubric, key) or Rubric(key=key)
    row.name = body.name
    row.dimensions = [d.model_dump() for d in body.dimensions]
    row.is_active = body.is_active
    db.add(row)
    db.commit()
    return row
