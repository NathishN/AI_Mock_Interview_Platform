from enum import StrEnum


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


class QuestionCategory(StrEnum):
    HR = "HR"
    BEHAVIORAL = "Behavioral"
    RESUME_PROJECTS = "Resume & Projects"
    PYTHON = "Python"
    SQL_ANALYTICS = "SQL & Analytics"
    ML_AI = "ML, AI & GenAI"
    COMPANY_WORKPLACE = "Company & Workplace"
    CODING = "Coding"
    JAVA_OOP = "Java & OOP"
    WEB_DEV = "Web Development"
    GIT_DEVOPS = "Git & CI/CD"
    NETWORKING_IOT = "Networking & IoT"
    OPERATING_SYSTEMS = "Operating Systems"
    APTITUDE = "Aptitude"


class Difficulty(StrEnum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class QuestionType(StrEnum):
    """Decides which default rubric applies to a question."""

    TECHNICAL = "technical"
    HR = "hr"
    CODING = "coding"


class SessionStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class TurnStatus(StrEnum):
    ASKED = "asked"
    EVALUATED = "evaluated"
    EVALUATION_FAILED = "evaluation_failed"


class InterviewStage(StrEnum):
    ONLINE_ASSESSMENT = "Online Assessment"
    TECHNICAL_SCREENING = "Technical Screening"
    TECHNICAL = "Technical"
    HR = "HR"
    MANAGERIAL = "Managerial"
    FINAL = "Final"


class TargetRole(StrEnum):
    SDE = "Software Development Engineer"
    PYTHON = "Python Developer"
    JAVA = "Java Developer"
    DATA_ANALYST = "Data Analyst"
    DATA_SCIENTIST = "Data Scientist"
    ML_ENGINEER = "Machine Learning Engineer"
    AI_ENGINEER = "AI Engineer"
    GENAI_ENGINEER = "Generative AI Engineer"
    FULL_STACK = "Full-Stack Developer"
    BACKEND = "Backend Developer"
    BUSINESS_ANALYST = "Business Analyst"
    OTHER = "Other"
