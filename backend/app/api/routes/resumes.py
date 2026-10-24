import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import desc, select

from app.api.deps import CurrentUser, DbSession
from app.models.resume import UserResume
from app.schemas.interview import InterviewSessionDetail
from app.schemas.resume import (
    EvaluateResumeQuestionIn,
    ResumeDetailOut,
    ResumeSummaryOut,
    ResumeTextUploadIn,
    StartResumeInterviewIn,
)
from app.services.ai_evaluator import evaluate_interview_answer
from app.services.interview_flow import start_interview_session
from app.services.resume_analyzer import (
    analyze_resume_and_generate_questions,
    extract_text_from_bytes,
)

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("/upload", response_model=ResumeDetailOut, status_code=status.HTTP_201_CREATED)
async def upload_resume_file(
    user: CurrentUser,
    db: DbSession,
    file: UploadFile = File(...),
    target_role: str = Form("Software Development Engineer"),
) -> UserResume:
    """Uploads a PDF, DOCX, or TXT resume, extracts content, analyzes with AI, and generates tailored questions."""
    filename = file.filename or "resume.pdf"
    content = await file.read()
    file_size = len(content)

    if file_size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum allowed limit of 10MB.",
        )

    # Determine file type
    fname_lower = filename.lower()
    if fname_lower.endswith(".pdf"):
        file_type = "pdf"
    elif fname_lower.endswith(".docx"):
        file_type = "docx"
    elif fname_lower.endswith(".txt"):
        file_type = "txt"
    else:
        file_type = "pdf"

    extracted_text = extract_text_from_bytes(content, filename)
    if not extracted_text or len(extracted_text.strip()) < 40:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to extract text from the uploaded resume. Please verify the file is not scanned or password protected, or paste the text directly.",
        )

    # Run AI analysis and question generation
    result = analyze_resume_and_generate_questions(
        raw_text=extracted_text,
        target_role=target_role,
    )

    resume_entry = UserResume(
        user_id=user.id,
        filename=filename,
        file_type=file_type,
        file_size_bytes=file_size,
        raw_text=extracted_text,
        target_role=target_role,
        parsed_data=result.get("parsed_data", {}),
        analysis=result.get("analysis", {}),
        is_active=True,
    )

    db.add(resume_entry)
    db.commit()
    db.refresh(resume_entry)
    return resume_entry


@router.post("/upload-text", response_model=ResumeDetailOut, status_code=status.HTTP_201_CREATED)
def upload_resume_text(
    body: ResumeTextUploadIn,
    user: CurrentUser,
    db: DbSession,
) -> UserResume:
    """Accepts pasted raw resume text, analyzes with AI, and generates tailored questions."""
    if not body.raw_text or len(body.raw_text.strip()) < 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pasted resume text must contain at least 50 characters.",
        )

    result = analyze_resume_and_generate_questions(
        raw_text=body.raw_text,
        target_role=body.target_role,
    )

    resume_entry = UserResume(
        user_id=user.id,
        filename=body.filename,
        file_type="txt",
        file_size_bytes=len(body.raw_text.encode("utf-8")),
        raw_text=body.raw_text,
        target_role=body.target_role,
        parsed_data=result.get("parsed_data", {}),
        analysis=result.get("analysis", {}),
        is_active=True,
    )

    db.add(resume_entry)
    db.commit()
    db.refresh(resume_entry)
    return resume_entry


@router.get("/latest", response_model=ResumeDetailOut)
def get_latest_resume(
    user: CurrentUser,
    db: DbSession,
) -> UserResume:
    """Fetches user's latest active analyzed resume and generated questions."""
    stmt = (
        select(UserResume)
        .where(UserResume.user_id == user.id, UserResume.is_active == True)
        .order_by(desc(UserResume.created_at))
        .limit(1)
    )
    resume = db.scalars(stmt).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No uploaded resume found for user. Upload a resume to generate questions.",
        )
    return resume


@router.get("", response_model=list[ResumeSummaryOut])
def list_user_resumes(
    user: CurrentUser,
    db: DbSession,
) -> list[UserResume]:
    """Lists history of user's uploaded resumes."""
    stmt = (
        select(UserResume)
        .where(UserResume.user_id == user.id, UserResume.is_active == True)
        .order_by(desc(UserResume.created_at))
    )
    resumes = list(db.scalars(stmt).all())
    for r in resumes:
        if r.analysis and isinstance(r.analysis, dict):
            r.ats_score = r.analysis.get("ats_score")
    return resumes


@router.get("/{resume_id}", response_model=ResumeDetailOut)
def get_resume_detail(
    resume_id: uuid.UUID,
    user: CurrentUser,
    db: DbSession,
) -> UserResume:
    """Fetches full breakdown, ATS score, and generated questions for a specific resume."""
    resume = db.get(UserResume, resume_id)
    if not resume or resume.user_id != user.id or not resume.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    return resume


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: uuid.UUID,
    user: CurrentUser,
    db: DbSession,
) -> None:
    """Soft-deletes an uploaded resume."""
    resume = db.get(UserResume, resume_id)
    if not resume or resume.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    resume.is_active = False
    db.commit()


@router.post("/{resume_id}/start-interview", response_model=InterviewSessionDetail, status_code=status.HTTP_201_CREATED)
def start_resume_interview(
    resume_id: uuid.UUID,
    body: StartResumeInterviewIn,
    user: CurrentUser,
    db: DbSession,
) -> InterviewSessionDetail:
    """Starts a real mock interview session populated with questions tailored to this resume."""
    resume = db.get(UserResume, resume_id)
    if not resume or resume.user_id != user.id or not resume.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    config = {
        "mode": "resume",
        "preset": "resume_round",
        "resume_id": str(resume.id),
        "target_role": body.target_role or resume.target_role or "Software Development Engineer",
        "company": body.company or "Target Tech Company",
        "num_questions": body.num_questions or 5,
        "difficulty": "Intermediate",
    }

    session = start_interview_session(
        db=db,
        user_id=user.id,
        config=config,
    )
    return session


@router.post("/{resume_id}/evaluate-question")
def evaluate_resume_question(
    resume_id: uuid.UUID,
    body: EvaluateResumeQuestionIn,
    user: CurrentUser,
    db: DbSession,
) -> dict[str, Any]:
    """Evaluates an individual answer to a resume-tailored question with deterministic rubrics and AI coaching."""
    resume = db.get(UserResume, resume_id)
    if not resume or resume.user_id != user.id or not resume.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    # Match question in resume's generated questions if available
    ref_answer = ""
    key_points: list[str] = []
    eval_criteria: list[str] = []
    category = "Resume & Projects"

    if resume.analysis and isinstance(resume.analysis, dict):
        gen_qs = resume.analysis.get("generated_questions", [])
        matched = next(
            (q for q in gen_qs if q.get("id") == body.question_id or q.get("question") == body.question_text),
            None,
        )
        if matched:
            ref_answer = matched.get("ideal_answer_outline", "")
            key_points = matched.get("key_points", [])
            category = matched.get("category", "Resume & Projects")
            if matched.get("interviewer_context"):
                eval_criteria = [matched["interviewer_context"]]

    target_role = body.target_role or resume.target_role or "Software Development Engineer"

    result = evaluate_interview_answer(
        question_text=body.question_text,
        answer_text=body.answer_text,
        rubric_key=body.rubric_key or "technical",
        reference_answer=ref_answer,
        key_points=key_points,
        evaluation_criteria=eval_criteria,
        difficulty="Intermediate",
        target_role=target_role,
    )
    return result
