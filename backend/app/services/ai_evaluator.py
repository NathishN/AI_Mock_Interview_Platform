import json
import logging
import re
import time
from typing import Any

from app.core.config import get_settings
from app.services.rubrics import DEFAULT_RUBRICS

logger = logging.getLogger(__name__)


def get_performance_band(score: float) -> str:
    """Coaching performance bands based on weighted score (0-100)."""
    if score >= 90.0:
        return "Excellent"
    if score >= 80.0:
        return "Strong"
    if score >= 70.0:
        return "Good, with improvement areas"
    if score >= 60.0:
        return "Needs targeted improvement"
    return "Requires additional practice"


def calculate_deterministic_score(dimension_scores: list[dict], rubric_dims: list[dict]) -> tuple[float, list[dict]]:
    """Calculates weighted total score on a 100-point scale deterministically.
    
    Formula: Each dimension score (0-10) multiplied by its weight (%).
    Contribution = (score / 10.0) * weight.
    Sum of weights is 100.0, so sum of contributions is 0-100.0.
    """
    weight_map = {d["name"].lower(): float(d["weight"]) for d in rubric_dims}
    validated_dims = []
    total_score = 0.0

    for dim in dimension_scores:
        name = dim.get("name", "General")
        dim_key = name.lower()
        weight = weight_map.get(dim_key, dim.get("weight", 20.0))
        # Clamp score between 0.0 and 10.0
        raw_score = float(dim.get("score", 5.0))
        clamped_score = max(0.0, min(10.0, round(raw_score, 1)))
        justification = dim.get("justification", "Evaluated based on standard criteria.")

        contribution = (clamped_score / 10.0) * weight
        total_score += contribution

        validated_dims.append({
            "name": name,
            "score": clamped_score,
            "weight": weight,
            "justification": justification,
        })

    final_score = max(0.0, min(100.0, round(total_score, 1)))
    return final_score, validated_dims


def _clean_json_text(text: str) -> str:
    """Strip markdown code fence if model wrapped output in ```json ... ```."""
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    return text


def _evaluate_heuristic_fallback(
    question_text: str,
    answer_text: str,
    reference_answer: str,
    rubric_dims: list[dict],
    key_points: list[str] | None = None,
) -> dict[str, Any]:
    """Deterministic semantic scoring fallback when Groq is unreachable or not configured.
    
    Ensures tests and local offline development operate seamlessly.
    """
    answer_words = set(re.findall(r"\w+", answer_text.lower()))
    ref_words = set(re.findall(r"\w+", reference_answer.lower()))

    # Basic word overlap ratio and length adequacy
    word_count = len(answer_text.split())
    overlap = len(answer_words & ref_words) / max(len(ref_words), 1)

    # Base dimension marks (0-10)
    dimension_scores = []
    base_mark = 5.0
    if word_count > 15:
        base_mark += 1.5
    if word_count > 50:
        base_mark += 1.0
    if overlap > 0.15:
        base_mark += 1.0
    if overlap > 0.35:
        base_mark += 1.0

    base_mark = min(9.0, max(3.0, base_mark))

    for dim in rubric_dims:
        dimension_scores.append({
            "name": dim["name"],
            "score": base_mark,
            "weight": dim["weight"],
            "justification": f"Candidate demonstrated adequate response addressing {dim['name'].lower()}.",
        })

    final_score, validated_dims = calculate_deterministic_score(dimension_scores, rubric_dims)

    return {
        "overall_score": final_score,
        "performance_band": get_performance_band(final_score),
        "dimension_scores": validated_dims,
        "strengths": [
            "Good attempt at structuring the core response.",
            "Addressed key aspects of the question clearly.",
        ],
        "missing_points": [
            "Could expand on technical trade-offs or specific edge cases.",
            "Providing a concrete real-world metric or example would strengthen the answer.",
        ],
        "mistakes": [],
        "clarity_feedback": "The explanation is understandable. Try to be more concise and lead with the key takeaway.",
        "ideal_answer": reference_answer,
        "improved_answer": (
            f"Here is a structured revision:\n{answer_text}\n\nKey enhancement: Structure using concise points "
            f"and support with specific results or complexity bounds."
        ),
        "follow_up_question": "Can you elaborate on how you would handle performance bottlenecks in this approach?",
        "practice_recommendations": [
            "Practice articulating technical rationale with specific complexity trade-offs.",
            "Review the STAR framework for situational and behavioral explanations.",
        ],
        "eval_model": "deterministic-heuristic-fallback",
        "eval_latency_ms": 15,
        "eval_prompt_tokens": 0,
        "eval_completion_tokens": 0,
    }


def evaluate_interview_answer(
    question_text: str,
    answer_text: str,
    rubric_key: str = "technical",
    reference_answer: str = "",
    key_points: list[str] | None = None,
    evaluation_criteria: list[str] | None = None,
    difficulty: str = "Intermediate",
    target_role: str = "Software Development Engineer",
) -> dict[str, Any]:
    """Evaluates an interview answer using Groq LLM inference with fallback.
    
    Adheres strictly to the evaluation engine specification:
    - Structured JSON output.
    - Deterministic backend calculation of final mark on 100-point scale.
    - Performance band mapping.
    - Latency and token tracking.
    """
    settings = get_settings()
    rubric_info = DEFAULT_RUBRICS.get(rubric_key, DEFAULT_RUBRICS["technical"])
    rubric_dims = rubric_info["dimensions"]

    if not settings.groq_api_key or settings.groq_api_key.strip() in {"", "dummy", "mock"}:
        return _evaluate_heuristic_fallback(
            question_text=question_text,
            answer_text=answer_text,
            reference_answer=reference_answer,
            rubric_dims=rubric_dims,
            key_points=key_points,
        )

    # Attempt Groq LLM evaluation
    start_time = time.perf_counter()
    rubric_desc = "\n".join(f"- {d['name']} (Weight: {d['weight']}%)" for d in rubric_dims)
    key_points_str = "\n".join(f"- {kp}" for kp in (key_points or []))
    criteria_str = "\n".join(f"- {ec}" for ec in (evaluation_criteria or []))

    system_prompt = (
        "You are an expert, objective technical interview evaluator and coach for Indian engineering students.\n"
        "Your task is to evaluate the candidate's answer fairly and constructively.\n"
        "Never score an answer solely by string matching against the reference answer; accept equivalent explanations, "
        "alternative valid architectures, and distinct valid phrasing.\n"
        "Score each dimension from 0.0 to 10.0 (where 10 is flawless and 0 is completely incorrect).\n"
        "Return STRICT valid JSON only, without commentary outside the JSON block."
    )

    user_prompt = f"""Target Role: {target_role}
Difficulty: {difficulty}
Rubric Type: {rubric_info['name']}

QUESTION:
{question_text}

REFERENCE ANSWER / CONCEPTS:
{reference_answer or "Use standard engineering and interview best practices."}

KEY POINTS TO LOOK FOR:
{key_points_str or "Standard correctness, clarity, and depth."}

EVALUATION CRITERIA:
{criteria_str or "Relevance, correctness, structure."}

RUBRIC DIMENSIONS:
{rubric_desc}

CANDIDATE'S SUBMITTED ANSWER:
\"\"\"{answer_text}\"\"\"

Generate a JSON object matching this exact schema:
{{
  "dimension_scores": [
    {{
      "name": "<Exact Dimension Name>",
      "score": <float 0.0 to 10.0>,
      "weight": <float weight matching rubric>,
      "justification": "<concise evidence-based rationale>"
    }}
  ],
  "strengths": ["<strength 1>", "<strength 2>"],
  "missing_points": ["<concept missed 1>"],
  "mistakes": ["<factual inaccuracy if any>"],
  "clarity_feedback": "<concise feedback on communication, brevity, and structure>",
  "ideal_answer": "<concise, top-tier model answer>",
  "improved_answer": "<enhanced version of the candidate's answer preserving their intent>",
  "follow_up_question": "<insightful follow-up question probing depth or trade-offs>",
  "practice_recommendations": ["<targeted study recommendation 1>"]
}}"""

    attempts = 0
    max_retries = max(1, settings.groq_max_retries)
    last_err: Exception | None = None

    while attempts < max_retries:
        attempts += 1
        try:
            from groq import Groq

            client = Groq(api_key=settings.groq_api_key, timeout=settings.groq_timeout_seconds)
            completion = client.chat.completions.create(
                model=settings.groq_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                response_format={"type": "json_object"},
            )

            latency_ms = int((time.perf_counter() - start_time) * 1000)
            raw_content = completion.choices[0].message.content or "{}"
            parsed = json.loads(_clean_json_text(raw_content))

            # Deterministic backend scoring
            dimension_scores = parsed.get("dimension_scores", [])
            final_score, validated_dims = calculate_deterministic_score(dimension_scores, rubric_dims)

            prompt_tokens = getattr(completion.usage, "prompt_tokens", None)
            completion_tokens = getattr(completion.usage, "completion_tokens", None)

            return {
                "overall_score": final_score,
                "performance_band": get_performance_band(final_score),
                "dimension_scores": validated_dims,
                "strengths": parsed.get("strengths", []),
                "missing_points": parsed.get("missing_points", []),
                "mistakes": parsed.get("mistakes", []),
                "clarity_feedback": parsed.get("clarity_feedback", "Clear communication."),
                "ideal_answer": parsed.get("ideal_answer", reference_answer),
                "improved_answer": parsed.get("improved_answer", ""),
                "follow_up_question": parsed.get("follow_up_question"),
                "practice_recommendations": parsed.get("practice_recommendations", []),
                "eval_model": settings.groq_model,
                "eval_latency_ms": latency_ms,
                "eval_prompt_tokens": prompt_tokens,
                "eval_completion_tokens": completion_tokens,
            }

        except Exception as e:
            last_err = e
            logger.warning(f"Groq evaluation attempt {attempts} failed: {e}")

    logger.error(f"All Groq evaluation attempts failed. Falling back to heuristic scoring: {last_err}")
    # Fallback gracefully rather than crash the session
    fallback = _evaluate_heuristic_fallback(
        question_text=question_text,
        answer_text=answer_text,
        reference_answer=reference_answer,
        rubric_dims=rubric_dims,
        key_points=key_points,
    )
    fallback["eval_error"] = str(last_err)[:250] if last_err else "Model call failed"
    return fallback
