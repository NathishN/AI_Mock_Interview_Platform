from fastapi import APIRouter
from pydantic import BaseModel

from app.api.deps import CurrentUser, DbSession
from app.models.user import UserProfile

router = APIRouter(prefix="/roadmap", tags=["roadmap"])


class Milestone(BaseModel):
    week: int
    title: str
    focus: str
    estimated_hours: int
    topics: list[str]
    practice_actions: list[str]
    completed: bool = False


class LearningRoadmap(BaseModel):
    target_role: str
    target_companies: list[str]
    total_weeks: int
    readiness_level: str
    milestones: list[Milestone]


@router.get("", response_model=LearningRoadmap)
def get_user_roadmap(user: CurrentUser, db: DbSession) -> LearningRoadmap:
    """Returns a tailored multi-week preparation roadmap aligned with the candidate's target role and profile."""
    profile = db.get(UserProfile, user.id)
    target_role = profile.target_role if profile and profile.target_role else "Software Development Engineer"
    preferred_companies = profile.preferred_companies if profile and profile.preferred_companies else ["TCS", "Infosys", "Amazon"]

    # Build milestones adapted to role
    if "data" in target_role.lower():
        milestones = [
            Milestone(
                week=1,
                title="SQL Querying & Database Mastery",
                focus="Technical Foundation",
                estimated_hours=12,
                topics=["SELECT, WHERE, GROUP BY, HAVING", "INNER/LEFT/RIGHT JOINs", "Window Functions (ROW_NUMBER, DENSE_RANK)", "Subqueries & CTEs"],
                practice_actions=["Solve 30 SQL questions in the Library", "Complete SQL Mock Interview session"],
            ),
            Milestone(
                week=2,
                title="Python for Data Analysis & Pandas",
                focus="Analytics Engineering",
                estimated_hours=14,
                topics=["Pandas data manipulation & cleaning", "Vectorized operations vs loops", "NumPy arrays & broadcasting", "Handling missing values"],
                practice_actions=["Answer 20 Python Data questions", "Build data cleaning pipeline project walkthrough"],
            ),
            Milestone(
                week=3,
                title="Data Storytelling & Business Metrics",
                focus="Analytical Reasoning",
                estimated_hours=10,
                topics=["KPI formulation (Churn, Retention, CAC)", "A/B testing basics", "Exploratory Data Analysis presentation", "Communicating insights to stakeholders"],
                practice_actions=["Practice 15 Business Case questions", "Draft EDA project explanation in HR Studio"],
            ),
            Milestone(
                week=4,
                title="HR, Behavioral & Final Interviews",
                focus="Selection Polish",
                estimated_hours=10,
                topics=["STAR framework for data projects", "Handling ambiguous stakeholder questions", "Salary negotiation & company fit", "Confidence & concise answers"],
                practice_actions=["Complete Full Mock Interview", "Polish Self-Introduction in HR Studio"],
            ),
        ]
    elif "ai" in target_role.lower() or "machine learning" in target_role.lower():
        milestones = [
            Milestone(
                week=1,
                title="Core ML Algorithms & Math Foundations",
                focus="Technical Foundations",
                estimated_hours=14,
                topics=["Supervised vs Unsupervised learning", "Bias-Variance tradeoff & Regularization", "Evaluation metrics (ROC-AUC, F1, PR-AUC)", "Tree models: Random Forest & XGBoost"],
                practice_actions=["Solve 25 ML questions in the Library", "Complete Technical Interview session on ML"],
            ),
            Milestone(
                week=2,
                title="Deep Learning & GenAI Fundamentals",
                focus="Advanced Architecture",
                estimated_hours=16,
                topics=["Embeddings & Vector Databases", "RAG architectures & Chunking strategies", "Prompt Engineering & Evaluation", "Hallucination reduction & Fine-tuning"],
                practice_actions=["Practice 25 GenAI questions in Library", "Prepare AI project walkthrough in HR Studio"],
            ),
            Milestone(
                week=3,
                title="ML Deployment & System Architecture",
                focus="Production Engineering",
                estimated_hours=12,
                topics=["FastAPI model serving", "Latency, throughput, and batching", "Data leakage prevention", "Responsible AI & Guardrails"],
                practice_actions=["Review 15 System Design questions", "Run Full Mock Interview with adaptive difficulty"],
            ),
            Milestone(
                week=4,
                title="HR & Behavioral Executive Rounds",
                focus="Final Selection",
                estimated_hours=8,
                topics=["Explaining complex ML to non-technical leaders", "STAR stories on project roadblocks", "Handling ethics & AI bias questions", "Career aspirations"],
                practice_actions=["Complete HR Round preset in Mock Room", "Save finalized drafts in HR Studio"],
            ),
        ]
    else:
        # Standard SDE / Full-Stack / Backend roadmap
        milestones = [
            Milestone(
                week=1,
                title="Data Structures & Algorithms Foundations",
                focus="Coding & Problem Solving",
                estimated_hours=15,
                topics=["Two-Pointer techniques & Sliding Window", "Binary Search & Sorting algorithms", "Hash maps & Frequency counters", "Stacks & Queues"],
                practice_actions=["Complete 25 Coding questions in the Library", "Practice solving problems in O(n) time"],
            ),
            Milestone(
                week=2,
                title="Object-Oriented Programming & Databases",
                focus="Core Computer Science",
                estimated_hours=12,
                topics=["4 Pillars of OOP with code examples", "Normalization & Database Indexing", "SQL Joins, Aggregations, & Transactions", "FastAPI / REST API design principles"],
                practice_actions=["Take a 30-min Technical Mock Interview", "Review 30 Python & SQL questions in Library"],
            ),
            Milestone(
                week=3,
                title="Resume Projects & Low-Level Architecture",
                focus="Project Defense",
                estimated_hours=12,
                topics=["Explaining technical project trade-offs", "Addressing security, scaling, and testing", "Debugging & Profiling with tracemalloc", "Concurrency and asynchronous programming"],
                practice_actions=["Draft project walkthrough in HR Studio", "Complete Weakness Improvement interview session"],
            ),
            Milestone(
                week=4,
                title="Company-Specific & HR Final Rounds",
                focus="Campus Placement Ready",
                estimated_hours=10,
                topics=["Amazon Leadership Principles & STAR method", "Company research for TCS/Infosys/Accenture", "Handling salary, relocation, and shift questions", "Eliminating overused clichés & buzzwords"],
                practice_actions=["Complete Full Mock Interview (45 mins)", "Refine Weakness & Strengths answers in HR Studio"],
            ),
        ]

    return LearningRoadmap(
        target_role=target_role,
        target_companies=preferred_companies,
        total_weeks=len(milestones),
        readiness_level="In Progress",
        milestones=milestones,
    )
