"""Validated, all-or-nothing bulk import. Used by the admin API and seed script,
so new questions never require application code changes."""

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Question, question_fingerprint
from app.schemas.question import ImportError_, ImportResult, QuestionCreate

_FIELDS = (
    "question", "subcategory", "reference_answer", "target_roles", "interview_stage",
    "key_points", "evaluation_criteria", "common_mistakes", "follow_up_questions",
    "tags", "rubric_key",
)


def _apply(row: Question, q: QuestionCreate) -> None:
    row.question = q.question
    row.question_hash = question_fingerprint(q.question)
    row.category = q.category.value
    row.difficulty = q.difficulty.value
    row.question_type = q.question_type.value
    for f in _FIELDS:
        if f in ("question",):
            continue
        value = getattr(q, f)
        if f == "interview_stage":
            value = [s.value for s in value]
        setattr(row, f, value)


def import_questions(
    db: Session, records: list[dict], update_existing: bool = True
) -> ImportResult:
    errors: list[ImportError_] = []
    valid: list[tuple[int, QuestionCreate]] = []
    seen_ids: dict[str, int] = {}
    seen_hashes: dict[str, int] = {}

    for i, raw in enumerate(records):
        rid = raw.get("id") if isinstance(raw, dict) else None
        try:
            q = QuestionCreate.model_validate(raw)
        except ValidationError as exc:
            msgs = [f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in exc.errors()]
            errors.append(ImportError_(index=i, id=rid if isinstance(rid, str) else None, errors=msgs))
            continue
        h = question_fingerprint(q.question)
        problems = []
        if q.id in seen_ids:
            problems.append(f"duplicate id (also at index {seen_ids[q.id]})")
        if h in seen_hashes:
            problems.append(f"duplicate question text (also at index {seen_hashes[h]})")
        if problems:
            errors.append(ImportError_(index=i, id=q.id, errors=problems))
            continue
        seen_ids[q.id], seen_hashes[h] = i, i
        valid.append((i, q))

    # Collisions with rows already in the database under a different id.
    if valid:
        hashes = {question_fingerprint(q.question): q.id for _, q in valid}
        rows = db.execute(
            select(Question.id, Question.question_hash).where(Question.question_hash.in_(list(hashes)))
        ).all()
        clash = {h: rid for rid, h in rows if hashes[h] != rid}
        for i, q in valid:
            h = question_fingerprint(q.question)
            if h in clash:
                errors.append(
                    ImportError_(index=i, id=q.id, errors=[f"same question text already stored as '{clash[h]}'"])
                )

    if errors:
        return ImportResult(ok=False, total_in_file=len(records), errors=errors)

    existing = {
        r.id: r
        for r in db.scalars(select(Question).where(Question.id.in_([q.id for _, q in valid])))
    }
    created = updated = skipped = 0
    for _, q in valid:
        row = existing.get(q.id)
        if row is not None and not update_existing:
            skipped += 1  # keep admin edits; seeding only adds missing questions
            continue
        if row is None:
            row = Question(id=q.id)
            db.add(row)
            created += 1
        else:
            updated += 1
        _apply(row, q)
    db.commit()
    return ImportResult(
        ok=True, created=created, updated=updated, skipped=skipped, total_in_file=len(records)
    )
