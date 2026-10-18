import uuid

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import desc, select

from app.api.deps import CurrentUser, DbSession
from app.models.interview import HRAnswerDraft
from app.schemas.hr_studio import (
    HRAnalysisOut,
    HRDraftIn,
    HRDraftOut,
    HRStudioAnalyzeIn,
    HRStudioGenerateIn,
    HRTopicInfo,
)
from app.services.hr_coach import (
    HR_TOPICS,
    analyze_hr_answer,
    generate_structured_hr_answer,
)

router = APIRouter(prefix="/hr-studio", tags=["hr-studio"])


@router.get("/topics", response_model=list[HRTopicInfo])
def get_hr_topics() -> list[dict]:
    """List dedicated HR training topics, frameworks, and structured guidance prompts."""
    return HR_TOPICS


@router.post("/generate")
def generate_hr_answer(body: HRStudioGenerateIn, user: CurrentUser) -> dict:
    """Generates a professional, structured interview answer strictly based on candidate-provided facts."""
    generated = generate_structured_hr_answer(topic_id=body.topic, facts=body.facts)
    return {
        "topic": body.topic,
        "generated_answer": generated,
    }


@router.post("/analyze", response_model=HRAnalysisOut)
def analyze_candidate_draft(body: HRStudioAnalyzeIn, user: CurrentUser) -> HRAnalysisOut:
    """Analyzes a candidate's HR draft answer for vagueness, buzzwords, and structure."""
    result = analyze_hr_answer(topic_id=body.topic, answer_text=body.answer_text)
    return HRAnalysisOut(**result)


@router.get("/drafts", response_model=list[HRDraftOut])
def list_drafts(user: CurrentUser, db: DbSession) -> list[HRAnswerDraft]:
    """Retrieve candidate's saved personal answer drafts."""
    stmt = (
        select(HRAnswerDraft)
        .where(HRAnswerDraft.user_id == user.id)
        .order_by(desc(HRAnswerDraft.updated_at))
    )
    return list(db.scalars(stmt).all())


@router.post("/drafts", response_model=HRDraftOut, status_code=status.HTTP_201_CREATED)
def save_draft(body: HRDraftIn, user: CurrentUser, db: DbSession) -> HRAnswerDraft:
    """Save or update an HR personal answer draft."""
    # Check if existing draft exists for this topic
    stmt = select(HRAnswerDraft).where(
        HRAnswerDraft.user_id == user.id,
        HRAnswerDraft.topic == body.topic,
    )
    existing = db.scalars(stmt).first()

    if existing:
        existing.facts = body.facts
        existing.generated_answer = body.generated_answer
        existing.final_answer = body.final_answer
        db.commit()
        db.refresh(existing)
        return existing

    draft = HRAnswerDraft(
        user_id=user.id,
        topic=body.topic,
        facts=body.facts,
        generated_answer=body.generated_answer,
        final_answer=body.final_answer,
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)
    return draft


@router.delete("/drafts/{draft_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_draft(draft_id: uuid.UUID, user: CurrentUser, db: DbSession) -> None:
    """Delete a saved HR answer draft."""
    draft = db.get(HRAnswerDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Draft not found")
    db.delete(draft)
    db.commit()
