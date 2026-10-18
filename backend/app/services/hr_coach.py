import json
import logging
import re
from typing import Any

from app.core.config import get_settings

logger = logging.getLogger(__name__)

HR_TOPICS: list[dict[str, Any]] = [
    {
        "id": "self_introduction",
        "title": "Tell me about yourself",
        "framework": "Present Status -> Relevant Skills -> Flagship Project -> Unique Strengths -> Career Direction",
        "description": "The foundational opener. Highlight your current academic/professional standing, core strengths, a flagship project, and why you are excited for this role.",
        "prompt_fields": [
            {"key": "degree_and_college", "label": "Degree & College / Branch", "placeholder": "B.Tech in Computer Science from XYZ University, 2025"},
            {"key": "key_skills", "label": "Top 2-3 Technical Skills", "placeholder": "Python, FastAPI, PostgreSQL, and Data Structures"},
            {"key": "flagship_project", "label": "Flagship Project & Impact", "placeholder": "Built an AI-assisted resume parser improving match rate by 30%"},
            {"key": "soft_strengths", "label": "Demonstrated Strengths", "placeholder": "Quick learner, strong debugging mindset, effective communicator"},
            {"key": "career_goal", "label": "Immediate Career Direction", "placeholder": "Looking to contribute as a Software Development Engineer building scalable systems"},
        ],
    },
    {
        "id": "why_hire_you",
        "title": "Why should we hire you?",
        "framework": "Core Competence -> Proof of Execution -> Fast Learning Ability -> Team Value Add",
        "description": "Differentiate yourself without sounding arrogant. Emphasize your solid fundamentals, practical project experience, and enthusiasm to deliver value from day one.",
        "prompt_fields": [
            {"key": "target_role", "label": "Target Role", "placeholder": "Associate Software Engineer"},
            {"key": "matching_strengths", "label": "Skills Matching Job Requirements", "placeholder": "Strong foundation in data structures, REST APIs, and backend databases"},
            {"key": "proof_of_effort", "label": "Tangible Proof / Accomplishment", "placeholder": "Consistently solved 300+ LeetCode problems and led college hackathon team"},
            {"key": "work_ethic", "label": "Adaptability & Work Ethic", "placeholder": "Eager to absorb mentorship, learn team conventions quickly, and take ownership"},
        ],
    },
    {
        "id": "weakness",
        "title": "What is your greatest weakness?",
        "framework": "Genuine Area -> Concrete Corrective Action -> Measurable Improvement (No Fake Weaknesses)",
        "description": "Never use fake weaknesses like 'I work too hard'. Pick a real, non-disqualifying technical or organizational skill and demonstrate active self-improvement.",
        "prompt_fields": [
            {"key": "genuine_weakness", "label": "Genuine Development Area", "placeholder": "Initially struggled with public speaking and presenting technical designs to large groups"},
            {"key": "action_taken", "label": "Concrete Steps You Took", "placeholder": "Volunteered to lead sprint demos and joined a public speaking student club"},
            {"key": "measurable_progress", "label": "Positive Current Result", "placeholder": "Recently delivered a 20-minute tech talk to 60+ peers with positive feedback"},
        ],
    },
    {
        "id": "why_this_company",
        "title": "Why do you want to join our company?",
        "framework": "Company Innovation -> Personal Resonance -> Alignment with Engineering Culture",
        "description": "Demonstrate that you researched the organization beyond generic website blurbs. Connect their engineering challenges to your personal career passions.",
        "prompt_fields": [
            {"key": "company_name", "label": "Company Name", "placeholder": "TCS / Amazon / Infosys / Google"},
            {"key": "company_achievement", "label": "Specific Product, Engineering Feat, or Value", "placeholder": "Your focus on scalable cloud architectures and open-source contributions"},
            {"key": "personal_alignment", "label": "Why This Inspires You", "placeholder": "I want to work on large-scale distributed systems impacting millions of users"},
        ],
    },
    {
        "id": "conflict_star",
        "title": "Tell me about a disagreement with a teammate (STAR)",
        "framework": "Situation -> Task -> Action (Diplomatic Communication) -> Result -> Key Learning",
        "description": "Showcases emotional intelligence, mature communication, and focusing on business outcomes over personal ego.",
        "prompt_fields": [
            {"key": "situation", "label": "Situation (Context)", "placeholder": "During our capstone project, teammate and I differed on whether to use SQL or NoSQL"},
            {"key": "task", "label": "Task (Objective)", "placeholder": "We needed to finalize the database schema without delaying project milestones"},
            {"key": "action", "label": "Action (What You Did)", "placeholder": "Created a benchmark comparison table assessing schema flexibility vs transaction needs, and discussed calmly"},
            {"key": "result", "label": "Result & Learning", "placeholder": "Agreed on PostgreSQL with JSONB; finished on time with high grades. Learned data-backed discussions resolve conflicts"},
        ],
    },
    {
        "id": "where_in_5_years",
        "title": "Where do you see yourself in five years?",
        "framework": "Technical Mastery -> Architectural Responsibility -> Mentorship & Growth",
        "description": "Demonstrates stability, commitment, and realistic ambition without overstepping into unrealistic executive claims.",
        "prompt_fields": [
            {"key": "primary_craft", "label": "Core Domain of Mastery", "placeholder": "Deepening my expertise in distributed backend systems and cloud infrastructure"},
            {"key": "leadership_aspect", "label": "Ownership & Mentorship", "placeholder": "Taking ownership of critical modules and mentoring incoming junior engineers"},
            {"key": "company_growth", "label": "Organizational Impact", "placeholder": "Becoming a reliable go-to engineer who drives resilient engineering practices"},
        ],
    },
]


def generate_structured_hr_answer(topic_id: str, facts: dict[str, Any]) -> str:
    """Assembles a natural, professional HR answer using candidate's facts without hallucination."""
    settings = get_settings()

    # If Groq key is present, polish with Groq
    if settings.groq_api_key and settings.groq_api_key.strip() not in {"", "dummy", "mock"}:
        try:
            from groq import Groq
            client = Groq(api_key=settings.groq_api_key, timeout=settings.groq_timeout_seconds)

            prompt = f"""You are an executive HR interview coach for Indian engineering students.
Generate a polished, professional, and natural first-person interview answer for the topic: '{topic_id}'.
RULES:
1. Rely EXCLUSIVELY on the candidate's provided facts below.
2. DO NOT hallucinate or invent new employers, achievements, test scores, or degrees.
3. Keep the tone humble, confident, concise, and structured.
4. Output ONLY the answer text, with no preamble or metadata.

FACTS PROVIDED BY CANDIDATE:
{json.dumps(facts, indent=2)}
"""
            completion = client.chat.completions.create(
                model=settings.groq_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            ans = completion.choices[0].message.content
            if ans and len(ans.strip()) > 20:
                return ans.strip()
        except Exception as e:
            logger.warning(f"Groq HR answer generation error: {e}")

    # High-quality deterministic templates based on topic
    if topic_id == "self_introduction":
        degree = facts.get("degree_and_college", "B.Tech in Computer Science")
        skills = facts.get("key_skills", "Python, data structures, and backend development")
        project = facts.get("flagship_project", "a full-stack web application with secure APIs")
        strengths = facts.get("soft_strengths", "quick learning and problem solving")
        goal = facts.get("career_goal", "contribute effectively as a software engineer")
        return (
            f"Hello and thank you for this opportunity. I am currently completing my {degree}. "
            f"Over the course of my academics, I have built strong fundamentals in {skills}. "
            f"One project I am particularly proud of is {project}, where I focused on building clean, efficient, and well-tested code. "
            f"What drives me is my {strengths}. As I take the next step in my professional journey, my immediate goal is to {goal}, "
            f"collaborate with experienced mentors, and deliver real impact."
        )

    if topic_id == "weakness":
        weakness = facts.get("genuine_weakness", "managing public speaking anxiety")
        action = facts.get("action_taken", "volunteered for sprint presentations and practice sessions")
        result = facts.get("measurable_progress", "gained significant confidence in explaining technical concepts")
        return (
            f"In the past, an area where I recognized a genuine need for improvement was {weakness}. "
            f"Rather than ignoring it, I took proactive steps: I {action}. "
            f"Because of this deliberate practice, I have {result}. "
            f"I continue to work on it consciously, and it has taught me the importance of continuous self-awareness."
        )

    if topic_id == "why_this_company":
        company = facts.get("company_name", "your esteemed organization")
        achievement = facts.get("company_achievement", "innovative engineering culture and large-scale client solutions")
        alignment = facts.get("personal_alignment", "tackling complex engineering challenges with high reliability")
        return (
            f"I have been closely following {company}, especially your work in {achievement}. "
            f"As an aspiring engineer, {alignment} is exactly the environment in which I want to grow. "
            f"Joining your team represents an opportunity to contribute with strong foundational rigor while learning from industry leaders."
        )

    if topic_id == "conflict_star":
        sit = facts.get("situation", "a project deadline disagreement")
        task = facts.get("task", "aligning on a technical choice without missing milestones")
        act = facts.get("action", "analyzed objective pros and cons together")
        res = facts.get("result", "achieved consensus and delivered the project on time")
        return (
            f"During our academic project, we encountered a situation where {sit}. "
            f"Our objective was clear: {task}. "
            f"To resolve this constructively, I {act}. "
            f"As a result, we {res}. This reinforced that transparent communication and data-driven discussions always produce the best outcomes."
        )

    # General fallback template
    fact_summary = ". ".join(f"{k.replace('_', ' ').capitalize()}: {v}" for k, v in facts.items() if v)
    return (
        f"Based on my preparation and background, {fact_summary}. "
        f"I am eager to apply these experiences, uphold high professional standards, and contribute meaningfully to the team."
    )


def analyze_hr_answer(topic_id: str, answer_text: str) -> dict[str, Any]:
    """Analyzes an HR answer draft for buzzwords, cliches, lack of concrete specifics, and structure."""
    words = re.findall(r"\w+", answer_text.lower())
    word_count = len(words)

    # Detect cliche buzzwords
    cliche_list = ["perfectionist", "workaholic", "hard worker", "passionate", "synergy", "think outside the box", "detail oriented"]
    found_cliches = [c for c in cliche_list if c in answer_text.lower()]

    # Detect presence of numbers / metrics (shows concrete specificity)
    has_metrics = bool(re.search(r"\b\d+[%+kKmM]?\b", answer_text))

    strengths = []
    vague_phrases = []
    coaching_tips = []

    if word_count >= 50 and word_count <= 250:
        strengths.append("Optimal answer length (concise, typically 1 to 2 minutes when spoken).")
    elif word_count < 50:
        vague_phrases.append("Answer is too brief and lacks supporting depth.")
        coaching_tips.append("Expand on specific actions you took or tools you used.")
    else:
        coaching_tips.append("The answer is somewhat verbose. Aim for 90-180 words to keep the interviewer engaged.")

    if has_metrics:
        strengths.append("Includes concrete evidence, numbers, or measurable indicators.")
    else:
        coaching_tips.append("Add a quantifiable indicator (e.g., team size, percentage improvement, line count, or timeframe).")

    if found_cliches:
        for c in found_cliches:
            vague_phrases.append(f"Cliché phrase detected: '{c}'")
        coaching_tips.append("Replace generic buzzwords with observable behaviors and concrete outcomes.")
    else:
        strengths.append("Avoided overused interview clichés.")

    # Score calculation (0-100)
    score = 70.0
    if strengths:
        score += len(strengths) * 7.0
    if found_cliches:
        score -= len(found_cliches) * 8.0
    if not has_metrics and word_count > 40:
        score -= 5.0
    score = max(30.0, min(95.0, round(score, 1)))

    return {
        "score": score,
        "strengths": strengths or ["Good direct tone answering the core question."],
        "vague_phrases": vague_phrases,
        "unsupported_claims": (
            ["Claim lacks verification; support with a specific project or role context."]
            if not has_metrics and word_count > 60
            else []
        ),
        "structure_feedback": (
            "Clear chronological flow with good introductory and concluding balance."
            if word_count > 40
            else "Ensure you establish context first, explain your action, and finish with your learning or impact."
        ),
        "coaching_tips": coaching_tips or ["Practice delivering this out loud smoothly with natural pauses."],
    }
