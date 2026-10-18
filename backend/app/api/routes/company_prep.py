from fastapi import APIRouter, HTTPException, status

from app.schemas.company_prep import CompanyOverview, CompanyRoundInfo

router = APIRouter(prefix="/company-prep", tags=["company-prep"])

COMPANIES: list[CompanyOverview] = [
    CompanyOverview(
        id="tcs",
        name="Tata Consultancy Services",
        slug="tcs",
        logo_letter="T",
        category="IT Services",
        difficulty="Moderate",
        hiring_rounds=3,
        description="India's largest IT employer, hiring through NQT for Ninja (3.36 LPA), Digital (7 LPA), and Prime (9 LPA) cadres.",
        rounds=[
            CompanyRoundInfo(
                round_number=1,
                name="TCS National Qualifier Test (NQT)",
                stage="Online Assessment",
                duration_minutes=120,
                description="Numerical ability, verbal reasoning, reasoning ability, and 2 hands-on coding problems.",
                focus_areas=["Aptitude", "String manipulation", "Array algorithms", "Time complexity"],
            ),
            CompanyRoundInfo(
                round_number=2,
                name="Technical Interview",
                stage="Technical",
                duration_minutes=35,
                description="In-depth discussion on projects, core languages (Python/Java/C++), DBMS concepts, and SQL queries.",
                focus_areas=["OOP concepts", "SQL joins & subqueries", "Final year project architecture", "Data structures"],
            ),
            CompanyRoundInfo(
                round_number=3,
                name="Managerial & HR Round",
                stage="HR & Managerial",
                duration_minutes=20,
                description="Evaluating flexibility, willingness to relocate, shift adaptability, communication, and background verification.",
                focus_areas=["Relocation willingness", "Conflict handling", "Why TCS", "Career goals"],
            ),
        ],
        key_tips=[
            "Be crystal clear on your resume projects—explain your exact contribution without exaggerating.",
            "Prepare basic SQL (JOINS, second-highest salary, aggregations) and OOP principles thoroughly.",
            "Display flexibility regarding location, shifts, and tech stacks during the HR round.",
        ],
        recommended_question_categories=["HR", "Python", "SQL & Analytics", "Company & Workplace"],
    ),
    CompanyOverview(
        id="infosys",
        name="Infosys",
        slug="infosys",
        logo_letter="I",
        category="IT Services",
        difficulty="Moderate to High",
        hiring_rounds=3,
        description="Major technology multinational hiring System Engineers (3.6 LPA), DSE (6.25 LPA), and Specialist Programmers (9.5 LPA).",
        rounds=[
            CompanyRoundInfo(
                round_number=1,
                name="Online Assessment / HackWithInfy",
                stage="Online Assessment",
                duration_minutes=100,
                description="Mathematical ability, logical reasoning, verbal ability, and pseudocode/coding questions.",
                focus_areas=["Aptitude", "Pseudocode analysis", "Dynamic programming (for SP role)"],
            ),
            CompanyRoundInfo(
                round_number=2,
                name="Technical Interview",
                stage="Technical",
                duration_minutes=40,
                description="Focuses heavily on Object-Oriented Programming, data structures, algorithms, and resume projects.",
                focus_areas=["OOP in Python/Java", "Linked lists, stacks, trees", "Resume project walkthrough"],
            ),
            CompanyRoundInfo(
                round_number=3,
                name="HR Interview",
                stage="HR",
                duration_minutes=15,
                description="Evaluates communication, adaptability, teamwork, and alignment with corporate values.",
                focus_areas=["Self introduction", "Handling constructive criticism", "Relocation & shift agreement"],
            ),
        ],
        key_tips=[
            "Know your OOP pillars (Encapsulation, Inheritance, Polymorphism, Abstraction) with real-life code examples.",
            "Explain code logic step-by-step; interviewers value your structured thought process as much as the final syntax.",
            "For DSE / SP tracks, practice intermediate graph algorithms and dynamic programming.",
        ],
        recommended_question_categories=["Python", "Coding", "HR", "Resume & Projects"],
    ),
    CompanyOverview(
        id="amazon",
        name="Amazon",
        slug="amazon",
        logo_letter="A",
        category="Product / Cloud",
        difficulty="High",
        hiring_rounds=4,
        description="Global tech titan hiring Software Development Engineers (SDE-1) with a dual focus on rigorous DSA and Amazon Leadership Principles.",
        rounds=[
            CompanyRoundInfo(
                round_number=1,
                name="Online Assessment (OA1 & OA2)",
                stage="Online Assessment",
                duration_minutes=90,
                description="2 algorithmic coding problems on HackerRank followed by an interactive Workstyles Assessment evaluating Amazon Leadership Principles.",
                focus_areas=["Arrays & Strings", "Trees & Graphs", "Dynamic Programming", "Amazon Leadership Principles"],
            ),
            CompanyRoundInfo(
                round_number=2,
                name="Technical Round 1 (DSA)",
                stage="Technical",
                duration_minutes=60,
                description="Live problem-solving on data structures and algorithms with strict time and space complexity scrutiny.",
                focus_areas=["Sliding window", "Monotonic stacks", "BFS/DFS", "Binary search"],
            ),
            CompanyRoundInfo(
                round_number=3,
                name="Technical Round 2 (OOP & Data Structures)",
                stage="Technical",
                duration_minutes=60,
                description="Low-level design / Object-Oriented Design alongside advanced algorithmic problem solving.",
                focus_areas=["Object-Oriented Design", "Design patterns", "Heaps & priority queues"],
            ),
            CompanyRoundInfo(
                round_number=4,
                name="Bar Raiser Interview",
                stage="Final & Behavioral",
                duration_minutes=60,
                description="Conducted by an independent Bar Raiser testing Customer Obsession, Ownership, Bias for Action, and Deliver Results via the STAR method.",
                focus_areas=["STAR format behavioral answers", "Handling failure & setbacks", "Disagree and commit"],
            ),
        ],
        key_tips=[
            "Master the STAR method for behavioral answers; tie every story to at least one Amazon Leadership Principle.",
            "Always state brute-force time complexity first, then optimize and write clean, production-grade code with zero syntax errors.",
            "Test your code against edge cases (empty lists, duplicates, negative numbers) before telling the interviewer you are done.",
        ],
        recommended_question_categories=["Coding", "Behavioral", "Resume & Projects", "Company & Workplace"],
    ),
    CompanyOverview(
        id="google",
        name="Google",
        slug="google",
        logo_letter="G",
        category="Product / AI",
        difficulty="Very High",
        hiring_rounds=4,
        description="Pioneer in AI, distributed computing, and web search hiring Software Engineers (L3) based on deep computer science fundamentals and Googliness.",
        rounds=[
            CompanyRoundInfo(
                round_number=1,
                name="Google Online Challenge",
                stage="Online Assessment",
                duration_minutes=90,
                description="2 challenging algorithmic problems testing combinatorial reasoning, graph theory, or advanced data structures.",
                focus_areas=["Graph algorithms", "Dynamic programming", "Prefix trees / Tries", "Bit manipulation"],
            ),
            CompanyRoundInfo(
                round_number=2,
                name="Coding Interview 1",
                stage="Technical",
                duration_minutes=45,
                description="Interactive problem solving on a shared Google Doc without syntax highlighting or autocompletion.",
                focus_areas=["Tree traversals", "Recursion", "Mathematical algorithms", "Complexity proofs"],
            ),
            CompanyRoundInfo(
                round_number=3,
                name="Coding Interview 2",
                stage="Technical",
                duration_minutes=45,
                description="A complex problem with evolving constraints and ambiguity to test your adaptability and analytical depth.",
                focus_areas=["Graph shortest paths", "Sliding window", "State space search"],
            ),
            CompanyRoundInfo(
                round_number=4,
                name="Googliness & Leadership",
                stage="Behavioral",
                duration_minutes=45,
                description="Evaluates intellectual humility, ethics, bias for action, collaborating in ambiguous environments, and teamwork.",
                focus_areas=["Receiving feedback", "Ethical decision making", "Supporting teammates"],
            ),
        ],
        key_tips=[
            "Communicate continuously—explain what you are thinking before you write a single line of code.",
            "Ask clarifying questions to resolve edge cases and ambiguities before designing an algorithm.",
            "Demonstrate 'Googliness': intellectual humility, receptiveness to hints, and passion for doing the right thing.",
        ],
        recommended_question_categories=["Coding", "Behavioral", "Python", "ML, AI & GenAI"],
    ),
    CompanyOverview(
        id="accenture",
        name="Accenture",
        slug="accenture",
        logo_letter="A",
        category="Consulting & Tech",
        difficulty="Moderate",
        hiring_rounds=3,
        description="Global professional services leader hiring Associate Software Engineers (4.5 LPA) and Advanced ASE (6.5 LPA).",
        rounds=[
            CompanyRoundInfo(
                round_number=1,
                name="Cognitive & Technical Assessment",
                stage="Online Assessment",
                duration_minutes=90,
                description="Critical thinking, analytical reasoning, technical aptitude (cloud, network security, pseudocode), and hands-on coding.",
                focus_areas=["Reasoning", "Cloud basics", "Network fundamentals", "Basic coding"],
            ),
            CompanyRoundInfo(
                round_number=2,
                name="Communication Assessment",
                stage="Voice Assessment",
                duration_minutes=20,
                description="Automated spoken English evaluation assessing pronunciation, fluency, vocabulary, and active listening.",
                focus_areas=["Spoken English fluency", "Listening comprehension", "Sentence repetition"],
            ),
            CompanyRoundInfo(
                round_number=3,
                name="Interview (Technical + HR)",
                stage="Interview",
                duration_minutes=25,
                description="A combined discussion assessing project knowledge, adaptability, willingness to learn new technologies, and cultural fit.",
                focus_areas=["Resume projects", "Agility and adaptability", "Situational judgment"],
            ),
        ],
        key_tips=[
            "Ensure a quiet room and clear microphone for the automated communication round.",
            "Show enthusiasm for learning enterprise technologies and cross-functional collaboration.",
            "Have a well-structured summary of your final-year project ready to share.",
        ],
        recommended_question_categories=["HR", "Company & Workplace", "SQL & Analytics", "Resume & Projects"],
    ),
]


@router.get("", response_model=list[CompanyOverview])
def list_companies() -> list[CompanyOverview]:
    """Lists company interview preparation guides and hiring patterns."""
    return COMPANIES


@router.get("/{company_slug}", response_model=CompanyOverview)
def get_company_detail(company_slug: str) -> CompanyOverview:
    """Fetches round-by-round interview breakdown, focus areas, and key coaching tips for a specific company."""
    comp = next((c for c in COMPANIES if c.slug.lower() == company_slug.lower()), None)
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company guide '{company_slug}' not found")
    return comp
