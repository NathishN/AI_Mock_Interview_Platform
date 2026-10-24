import random
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import Difficulty, SessionStatus, TurnStatus
from app.models.interview import InterviewSession, InterviewTurn
from app.models.question import Question
from app.models.resume import UserResume
from app.services.ai_evaluator import evaluate_interview_answer, get_performance_band


CATEGORY_MAP = {
    "technical": [
        "Python", "SQL & Analytics", "ML, AI & GenAI", "Resume & Projects",
        "Java & OOP", "Web Development", "Git & CI/CD", "Networking & IoT",
    ],
    "hr": ["HR", "Company & Workplace"],
    "behavioral": ["Behavioral"],
    "coding": ["Coding", "Java & OOP"],
    "mixed": [
        "HR", "Behavioral", "Resume & Projects", "Python", "SQL & Analytics",
        "ML, AI & GenAI", "Company & Workplace", "Coding",
        "Java & OOP", "Web Development", "Git & CI/CD", "Networking & IoT",
    ],
    "resume": ["Resume & Projects", "Technical", "Behavioral"],
}

RUBRIC_FOR_CATEGORY = {
    "HR": "hr",
    "Behavioral": "hr",
    "Company & Workplace": "hr",
    "Coding": "coding",
    "Python": "technical",
    "SQL & Analytics": "technical",
    "ML, AI & GenAI": "technical",
    "Resume & Projects": "technical",
    "Technical": "technical",
    "Java & OOP": "technical",
    "Web Development": "technical",
    "Git & CI/CD": "technical",
    "Networking & IoT": "technical",
}

PRESET_CONFIGS = {
    "resume_round": {
        "duration_minutes": 25,
        "interview_stage": "Technical",
        "mode": "resume",
        "num_questions": 5,
        "difficulty": "Intermediate",
    },
    "hr_round": {
        "duration_minutes": 15,
        "interview_stage": "HR",
        "mode": "hr",
        "num_questions": 4,
        "difficulty": "Beginner",
    },
    "final_interview": {
        "duration_minutes": 20,
        "interview_stage": "Final",
        "mode": "mixed",
        "num_questions": 5,
        "difficulty": "Intermediate",
    },
    "technical_interview": {
        "duration_minutes": 30,
        "interview_stage": "Technical",
        "mode": "technical",
        "num_questions": 6,
        "difficulty": "Intermediate",
    },
    "full_mock": {
        "duration_minutes": 45,
        "interview_stage": "Technical",
        "mode": "mixed",
        "num_questions": 8,
        "difficulty": "Intermediate",
    },
    "weakness_improvement": {
        "duration_minutes": 15,
        "interview_stage": "Technical",
        "mode": "mixed",
        "num_questions": 4,
        "difficulty": "Beginner",
    },
}


def _select_candidate_questions(
    db: Session,
    mode: str,
    target_role: str,
    difficulty: str,
    count: int,
) -> list[Question]:
    """Selects suitable questions from the database."""
    categories = CATEGORY_MAP.get(mode, CATEGORY_MAP["mixed"])
    stmt = select(Question).where(Question.category.in_(categories), Question.is_active == True)
    all_questions = list(db.scalars(stmt).all())

    if not all_questions:
        # Fallback to any active question
        all_questions = list(db.scalars(select(Question).where(Question.is_active == True)).all())

    # Prioritize role and difficulty matches
    scored_questions = []
    for q in all_questions:
        score = 0
        if q.difficulty == difficulty:
            score += 2
        if any(target_role.lower() in r.lower() for r in (q.target_roles or [])):
            score += 3
        scored_questions.append((score, random.random(), q))

    scored_questions.sort(key=lambda x: (x[0], x[1]), reverse=True)
    selected = [item[2] for item in scored_questions[:count]]
    random.shuffle(selected)
    return selected


def start_interview_session(
    db: Session,
    user_id: uuid.UUID,
    config: dict[str, Any],
) -> InterviewSession:
    """Initializes an interview session and prepares the first turn."""
    preset_name = config.get("preset")
    if preset_name and preset_name in PRESET_CONFIGS:
        # Merge preset defaults
        merged = dict(PRESET_CONFIGS[preset_name])
        merged.update(config)
        config = merged

    num_questions = config.get("num_questions", 5)
    mode = config.get("mode", "mixed")
    target_role = config.get("target_role", "Software Development Engineer")
    difficulty = config.get("difficulty", "Intermediate")

    # If resume mode is selected, load tailored questions from user's resume
    if mode == "resume" or config.get("resume_id"):
        resume_id_str = config.get("resume_id")
        resume: UserResume | None = None
        if resume_id_str:
            try:
                resume = db.get(UserResume, uuid.UUID(str(resume_id_str)))
            except Exception:
                resume = None
        if not resume:
            stmt = (
                select(UserResume)
                .where(UserResume.user_id == user_id, UserResume.is_active == True)
                .order_by(UserResume.created_at.desc())
                .limit(1)
            )
            resume = db.scalars(stmt).first()

        if resume and resume.analysis:
            resume_questions = list(resume.analysis.get("generated_questions", []))
            if resume_questions:
                config["resume_id"] = str(resume.id)
                config["resume_filename"] = resume.filename
                config["mode"] = "resume"
                first_rq = resume_questions[0]
                session = InterviewSession(
                    user_id=user_id,
                    status=SessionStatus.IN_PROGRESS.value,
                    config=config,
                    adaptive_state={
                        "running_scores": [],
                        "current_difficulty": first_rq.get("difficulty", difficulty),
                        "target_count": min(num_questions, len(resume_questions)),
                        "question_pool_ids": [],
                        "asked_question_ids": [],
                        "resume_questions": resume_questions,
                        "resume_index": 1,
                        "vagueness_count": 0,
                    },
                    started_at=datetime.now(timezone.utc),
                )
                db.add(session)
                db.flush()

                turn1 = InterviewTurn(
                    session_id=session.id,
                    sequence=1,
                    question_id=None,
                    question_text=first_rq["question"],
                    rubric_key=first_rq.get("rubric_key", "technical"),
                    difficulty=first_rq.get("difficulty", "Intermediate"),
                    topic=first_rq.get("topic", "Resume Deep Dive"),
                    status=TurnStatus.ASKED.value,
                )
                db.add(turn1)
                db.commit()
                db.refresh(session)
                return session

    selected_questions = _select_candidate_questions(
        db=db,
        mode=mode,
        target_role=target_role,
        difficulty=difficulty,
        count=max(num_questions, 5),
    )

    question_pool_ids = [q.id for q in selected_questions]

    session = InterviewSession(
        user_id=user_id,
        status=SessionStatus.IN_PROGRESS.value,
        config=config,
        adaptive_state={
            "running_scores": [],
            "current_difficulty": difficulty,
            "target_count": num_questions,
            "question_pool_ids": question_pool_ids,
            "asked_question_ids": [],
            "vagueness_count": 0,
        },
        started_at=datetime.now(timezone.utc),
    )
    db.add(session)
    db.flush()

    # Create Turn 1
    if selected_questions:
        first_q = selected_questions[0]
        rubric_key = RUBRIC_FOR_CATEGORY.get(first_q.category, "technical")
        turn1 = InterviewTurn(
            session_id=session.id,
            sequence=1,
            question_id=first_q.id,
            question_text=first_q.question,
            rubric_key=rubric_key,
            difficulty=first_q.difficulty,
            topic=first_q.subcategory or first_q.category,
            status=TurnStatus.ASKED.value,
        )
        session.adaptive_state["asked_question_ids"].append(first_q.id)
        db.add(turn1)
        db.commit()
        db.refresh(session)
    else:
        # Fallback question if DB empty
        turn1 = InterviewTurn(
            session_id=session.id,
            sequence=1,
            question_text="Tell me about yourself, your technical background, and your career goals.",
            rubric_key="hr",
            difficulty="Beginner",
            topic="Self Introduction",
            status=TurnStatus.ASKED.value,
        )
        db.add(turn1)
        db.commit()
        db.refresh(session)

    return session


def process_candidate_answer(
    db: Session,
    session: InterviewSession,
    turn: InterviewTurn,
    answer_text: str,
) -> tuple[InterviewTurn, InterviewSession]:
    """Evaluates the submitted answer, updates adaptive state, and advances turn."""
    turn.answer_text = answer_text
    turn.answered_at = datetime.now(timezone.utc)

    # Fetch reference question details if available
    ref_q: Question | None = None
    if turn.question_id:
        ref_q = db.get(Question, turn.question_id)

    target_role = session.config.get("target_role", "Software Development Engineer")

    ref_answer = ref_q.reference_answer if ref_q else ""
    key_points = ref_q.key_points if ref_q else []
    eval_criteria = ref_q.evaluation_criteria if ref_q else []

    if not ref_q and session.config.get("mode") == "resume":
        resume_questions = session.adaptive_state.get("resume_questions", [])
        matched = next((rq for rq in resume_questions if rq.get("question") == turn.question_text), None)
        if matched:
            ref_answer = matched.get("ideal_answer_outline", "")
            key_points = matched.get("key_points", [])
            if matched.get("interviewer_context"):
                eval_criteria = [matched["interviewer_context"]]

    eval_result = evaluate_interview_answer(
        question_text=turn.question_text,
        answer_text=answer_text,
        rubric_key=turn.rubric_key or "technical",
        reference_answer=ref_answer,
        key_points=key_points,
        evaluation_criteria=eval_criteria,
        difficulty=turn.difficulty or "Intermediate",
        target_role=target_role,
    )

    turn.evaluation = eval_result
    turn.overall_score = eval_result["overall_score"]
    turn.eval_model = eval_result.get("eval_model")
    turn.eval_latency_ms = eval_result.get("eval_latency_ms")
    turn.eval_prompt_tokens = eval_result.get("eval_prompt_tokens")
    turn.eval_completion_tokens = eval_result.get("eval_completion_tokens")
    turn.eval_error = eval_result.get("eval_error")
    turn.status = TurnStatus.EVALUATED.value

    # Update adaptive state
    adaptive_state = dict(session.adaptive_state or {})
    running_scores = list(adaptive_state.get("running_scores", []))
    running_scores.append(turn.overall_score)
    adaptive_state["running_scores"] = running_scores

    # Check for vagueness or short answer
    if len(answer_text.split()) < 20:
        adaptive_state["vagueness_count"] = adaptive_state.get("vagueness_count", 0) + 1

    # Dynamic difficulty adjustment
    curr_diff = adaptive_state.get("current_difficulty", Difficulty.INTERMEDIATE.value)
    if turn.overall_score >= 85.0:
        if curr_diff == Difficulty.BEGINNER.value:
            adaptive_state["current_difficulty"] = Difficulty.INTERMEDIATE.value
        elif curr_diff == Difficulty.INTERMEDIATE.value:
            adaptive_state["current_difficulty"] = Difficulty.ADVANCED.value
    elif turn.overall_score < 60.0:
        if curr_diff == Difficulty.ADVANCED.value:
            adaptive_state["current_difficulty"] = Difficulty.INTERMEDIATE.value
        elif curr_diff == Difficulty.INTERMEDIATE.value:
            adaptive_state["current_difficulty"] = Difficulty.BEGINNER.value

    session.adaptive_state = adaptive_state

    # Check if more questions should be asked
    target_count = int(session.config.get("num_questions", 5))
    asked_count = len(session.turns)

    if asked_count < target_count:
        # Determine if we should ask a follow-up or a fresh question
        follow_up_text = eval_result.get("follow_up_question")
        should_follow_up = False

        # If answer had missing points and a good follow-up exists, occasionally ask follow-up
        if follow_up_text and turn.overall_score < 75.0 and not turn.is_follow_up:
            should_follow_up = True

        if should_follow_up:
            next_turn = InterviewTurn(
                session_id=session.id,
                sequence=asked_count + 1,
                parent_turn_id=turn.id,
                question_text=follow_up_text,
                is_follow_up=True,
                rubric_key=turn.rubric_key,
                difficulty=adaptive_state.get("current_difficulty"),
                topic=f"Follow-up: {turn.topic or 'Deep Dive'}",
                status=TurnStatus.ASKED.value,
            )
            db.add(next_turn)
        else:
            if session.config.get("mode") == "resume":
                resume_questions = list(adaptive_state.get("resume_questions", []))
                resume_idx = int(adaptive_state.get("resume_index", 1))
                if resume_idx < len(resume_questions) and asked_count < target_count:
                    next_rq = resume_questions[resume_idx]
                    adaptive_state["resume_index"] = resume_idx + 1
                    session.adaptive_state = adaptive_state
                    next_turn = InterviewTurn(
                        session_id=session.id,
                        sequence=asked_count + 1,
                        question_id=None,
                        question_text=next_rq["question"],
                        rubric_key=next_rq.get("rubric_key", "technical"),
                        difficulty=next_rq.get("difficulty", "Intermediate"),
                        topic=next_rq.get("topic", "Resume Deep Dive"),
                        status=TurnStatus.ASKED.value,
                    )
                    db.add(next_turn)
                else:
                    conclude_interview_session(session)
            else:
                # Pick next question from pool or db
                pool = list(adaptive_state.get("question_pool_ids", []))
                asked_ids = set(adaptive_state.get("asked_question_ids", []))
                available = [qid for qid in pool if qid not in asked_ids]

                next_q: Question | None = None
                if available:
                    next_qid = available[0]
                    next_q = db.get(Question, next_qid)
                
                if not next_q:
                    # Query a new question from DB matching category
                    mode = session.config.get("mode", "mixed")
                    categories = CATEGORY_MAP.get(mode, CATEGORY_MAP["mixed"])
                    diff = adaptive_state.get("current_difficulty", Difficulty.INTERMEDIATE.value)
                    stmt = select(Question).where(
                        Question.category.in_(categories),
                        Question.id.not_in(list(asked_ids) or [""]),
                        Question.is_active == True,
                    )
                    candidates = list(db.scalars(stmt).all())
                    if candidates:
                        next_q = random.choice(candidates)

                if next_q:
                    rubric_key = RUBRIC_FOR_CATEGORY.get(next_q.category, "technical")
                    next_turn = InterviewTurn(
                        session_id=session.id,
                        sequence=asked_count + 1,
                        question_id=next_q.id,
                        question_text=next_q.question,
                        rubric_key=rubric_key,
                        difficulty=next_q.difficulty,
                        topic=next_q.subcategory or next_q.category,
                        status=TurnStatus.ASKED.value,
                    )
                    adaptive_state["asked_question_ids"].append(next_q.id)
                    session.adaptive_state = adaptive_state
                    db.add(next_turn)
                else:
                    # Conclude session if no more questions
                    conclude_interview_session(session)
    else:
        # Target question count reached
        conclude_interview_session(session)

    db.commit()
    db.refresh(session)
    db.refresh(turn)
    return turn, session


def conclude_interview_session(session: InterviewSession) -> InterviewSession:
    """Finalizes session, compiles comprehensive report, and sets status to COMPLETED."""
    evaluated_turns = [t for t in session.turns if t.overall_score is not None]
    if evaluated_turns:
        avg_score = round(sum(t.overall_score for t in evaluated_turns) / len(evaluated_turns), 1)
    else:
        avg_score = 0.0

    session.final_score = avg_score
    session.status = SessionStatus.COMPLETED.value
    session.ended_at = datetime.now(timezone.utc)

    # Dimension score aggregation
    dim_totals: dict[str, list[float]] = {}
    all_strengths: list[str] = []
    all_missing: list[str] = []
    all_recs: list[str] = []

    for t in evaluated_turns:
        ev = t.evaluation or {}
        for d in ev.get("dimension_scores", []):
            dname = d.get("name", "General")
            dim_totals.setdefault(dname, []).append(float(d.get("score", 5.0)))
        all_strengths.extend(ev.get("strengths", []))
        all_missing.extend(ev.get("missing_points", []))
        all_missing.extend(ev.get("mistakes", []))
        all_recs.extend(ev.get("practice_recommendations", []))

    dimension_breakdown = []
    for dname, scores in dim_totals.items():
        avg_dim = round(sum(scores) / len(scores), 1)
        dimension_breakdown.append({
            "dimension": dname,
            "average_mark": avg_dim,  # 0-10
            "percentage": round(avg_dim * 10.0, 1),  # 0-100%
        })

    session.report = {
        "final_score": avg_score,
        "performance_band": get_performance_band(avg_score),
        "total_questions": len(evaluated_turns),
        "dimension_breakdown": dimension_breakdown,
        "strengths": list(dict.fromkeys(all_strengths))[:5],
        "areas_for_improvement": list(dict.fromkeys(all_missing))[:5],
        "practice_recommendations": list(dict.fromkeys(all_recs))[:5],
    }

    return session
