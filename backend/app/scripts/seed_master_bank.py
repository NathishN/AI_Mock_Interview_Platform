"""Master Interview Question Bank Seeder
Consolidated from IBM, Hexaware, Payoda, SWS AI, AquaAirX & Wheelson Technologies interview experiences.
Covers Parts 1 through 12:
- Part 1: Self-Introduction, HR, Goals, Relocation, Shifts, AI Impact, GD
- Part 2: Resume, Projects, Workflow, Backend, Frontend, Testing, Internships, Research
- Part 3: Programming (Strings, Numbers, Arrays, Python Coding)
- Part 4: Python Internals & Advanced Topics
- Part 5: Java & Object-Oriented Programming (JVM, OOP Pillars, Overloading vs Overriding)
- Part 6: SQL & Databases (Indexes, ACID, Joins, Second-Highest Salary, Insert queries)
- Part 7: Git, GitHub, Version Control & CI/CD
- Part 8: Web Development (HTML/CSS, React, FastAPI, REST APIs, JWT, Supabase)
- Part 9: AI, Machine Learning, Deep Learning, RAG, and Agentic Systems
- Part 10: Networking, Cybersecurity, and IoT
- Part 11: Company-Specific Experiences (IBM, Hexaware, Payoda, SWS AI, AquaAirX, Wheelson)
- Part 12: Questions Freshers Should Ask the Interviewer
- Priority Tagging: Top 30 High-Priority Questions for Quick Revision
"""

import json
import logging
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.question import Question, question_fingerprint
from app.models.enums import QuestionCategory, Difficulty, QuestionType, InterviewStage
from app.schemas.question import QuestionCreate

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("seed_master_bank")

# Top 30 high-priority questions to highlight
TOP_30_KEYWORDS = {
    "tell me about yourself",
    "why should we hire you",
    "why do you want to join",
    "best project",
    "project architecture",
    "individual contribution",
    "challenges did you face",
    "strengths and weaknesses",
    "short-term and long-term",
    "willing to relocate",
    "palindrome program",
    "count vowels",
    "fibonacci",
    "number is prime",
    "second-largest",
    "reverse a string",
    "zeros to the end",
    "list, tuple, set",
    "four pillars of oop",
    "inheritance and method overriding",
    "difference between git and github",
    "ddl, dml, dcl",
    "sql joins",
    "second-highest salary",
    "database indexing",
    "overfitting and underfitting",
    "bias and variance",
    "prompt engineering versus fine-tuning",
    "rag and ai agents",
    "questions would you ask the interviewer",
}

MASTER_BANK_DATA = [
    # -------------------------------------------------------------
    # PART 1: SELF-INTRODUCTION AND HR QUESTIONS
    # -------------------------------------------------------------
    {
        "q": "Introduce yourself and explain your technical background.",
        "cat": "HR",
        "sub": "Self Introduction & Background",
        "d": "Beginner",
        "type": "hr",
        "roles": ["Software Development Engineer", "AI Engineer", "Python Developer", "Full-Stack Developer"],
        "stages": ["HR", "Technical Screening"],
        "ans": "A strong technical self-introduction should balance academic background, core programming proficiencies, hands-on project accomplishments, and career enthusiasm. Structure: 1) Brief greeting, degree, and university, 2) Technical core competencies: languages (Python, Java), frameworks (React, FastAPI), databases (PostgreSQL, Supabase), and domains (AI/ML or full-stack web), 3) Flagship project highlight: briefly state the business problem solved, tech stack, and verifiable result, 4) Practical exposure: internships, certifications, or open-source hackathons, and 5) Why you are eager for this role. Illustrative example: 'Good morning/afternoon. I recently completed my B.E. in Computer Science with a specialization in AI. Over the last four years, I've developed solid foundations in Python, Java, and relational database systems. My flagship project was an automated document analysis pipeline using FastAPI and vector embeddings that reduced manual review time by 60%. Beyond academics, I completed an internship where I built responsive React frontends and integrated REST APIs. I am excited to apply my hands-on problem-solving skills to scalable engineering challenges at your company.'",
        "kp": ["Structured flow: Education -> Core Tech Stack -> Flagship Project -> Industry Exposure -> Value Proposition", "Highlight practical engineering over generic buzzwords", "Keep duration between 90 and 120 seconds with confident delivery"],
        "crit": ["Clear, professional articulation without rambling", "Specific mention of relevant languages, frameworks, and real projects", "Coherent alignment with the hiring team's requirements"],
        "cm": ["Reciting the entire resume line by line", "Focusing exclusively on hobbies rather than technical achievements", "Speaking for more than 3 minutes without a clear conclusion"],
        "fu": ["What was the most challenging technical concept you learned during college?", "How do you keep your technical skills updated outside coursework?"],
        "tags": ["master-bank", "ibm", "hexaware", "aquaairx", "hr", "self-intro", "top-30"]
    },
    {
        "q": "What is the meaning of your name, and where are you from?",
        "cat": "HR",
        "sub": "Personal Background & Icebreaker",
        "d": "Beginner",
        "type": "hr",
        "roles": ["Software Development Engineer", "Data Analyst", "AI Engineer"],
        "stages": ["HR"],
        "ans": "Interviewers ask icebreaker questions to gauge cultural awareness, poise, communication clarity, and whether you are comfortable in spontaneous conversation. Answer smoothly: 1) State the origin and meaning of your name with pride and brevity, 2) Mention your hometown and one notable characteristic (cultural, industrial, or educational landmark), 3) Connect seamlessly back to your current professional journey in college. Illustrative example: 'My name means 'guide' or 'light' in Sanskrit, which inspires me to approach problem-solving with clarity and curiosity. I hail from Coimbatore, Tamil Nadu, popularly known as the Manchester of South India for its entrepreneurial spirit and textile engineering. Growing up in a hub of innovation motivated me to pursue Computer Science and build technology solutions.'",
        "kp": ["Clear, confident explanation of name origin and meaning", "Concise mention of hometown and its notable attributes", "Professional transition back to your enthusiasm for engineering"],
        "crit": ["Warm, natural demeanor without hesitation or defensiveness", "Concise articulation within 45 seconds"],
        "cm": ["Saying 'I don't know the meaning of my name'", "Giving an excessively long history lesson about your city", "Sounding nervous over a simple conversational icebreaker"],
        "fu": ["How has your hometown shaped your work ethic or personality?", "Are you comfortable relocating away from your hometown for this job?"],
        "tags": ["master-bank", "hexaware", "hr", "personal-background"]
    },
    {
        "q": "Are you a day scholar or a hosteller, and how has that shaped your daily routine?",
        "cat": "HR",
        "sub": "Adaptability & Lifestyle",
        "d": "Beginner",
        "type": "hr",
        "roles": ["Software Development Engineer", "AI Engineer"],
        "stages": ["HR"],
        "ans": "This question tests your time management, independence, adaptability, and peer collaboration skills. Both day scholars and hostellers have distinct strengths: If a day scholar: highlight discipline, commute management, and balancing family commitments with coursework and coding practice. If a hosteller: highlight self-reliance, cross-cultural peer collaboration, group study sessions, and independent problem-solving. Illustrative example (Hosteller): 'I lived in the college hostel for four years. Living away from home taught me self-discipline, time management, and the ability to collaborate closely with peers from diverse backgrounds during late-night hackathons and project sprints. It made me highly adaptable to new environments and team dynamics.'",
        "kp": ["Demonstrate time management discipline and personal ownership", "Highlight peer collaboration and adaptability to shared workspaces", "Positive, mature framing regardless of whether day scholar or hosteller"],
        "crit": ["Honest, authentic explanation showcasing independence and discipline", "Smooth delivery without complaints about food or commute"],
        "cm": ["Complaining excessively about hostel rules or long daily bus commutes", "Portraying a lack of discipline or irregular study habits"],
        "fu": ["How did you balance daily study with project deadlines?", "How do you manage independent living in a new city?"],
        "tags": ["master-bank", "hexaware", "aquaairx", "hr", "lifestyle"]
    },
    {
        "q": "Why did you choose Computer Science and Engineering over other branches?",
        "cat": "HR",
        "sub": "Career Motivation",
        "d": "Beginner",
        "type": "hr",
        "roles": ["Software Development Engineer", "AI Engineer", "Full-Stack Developer"],
        "stages": ["HR", "Technical Screening"],
        "ans": "Interviewers want to understand whether your choice was intentional and passion-driven or merely dictated by parental or peer pressure. Effective framework: 1) The initial spark: an early encounter with software, logic games, or seeing digital tools solve real human problems, 2) The instant gratification of code: the ability to design an idea and see it execute immediately on a screen, 3) Scalable impact: how software enables a small team to serve millions of users globally, and 4) Ongoing commitment: how coursework confirmed your passion through building practical applications. Illustrative example: 'During high school, I was fascinated by how a few lines of logic could automate repetitive tasks. When I wrote my first program and saw it solve a calculation instantly, I realized that software is modern leverage—it allows an engineer to create tangible impact with nothing more than logic and creativity. Choosing Computer Science gave me the formal foundation in data structures, algorithms, and system architecture to turn ideas into scalable digital products.'",
        "kp": ["Authentic intrinsic motivation rather than external herd mentality", "Appreciation for software leverage, logical thinking, and digital impact", "Continuity from college choice to actual hands-on projects completed"],
        "crit": ["Clarity of passion and purpose", "Coherent connection between interest and technical accomplishments"],
        "cm": ["Saying 'My parents told me to take CSE' or 'It has the highest campus salaries'", "Failing to connect your choice with what you actually built in college"],
        "fu": ["Which computer science subject did you enjoy most and why?", "How do you feel about the rapid changes in programming frameworks?"],
        "tags": ["master-bank", "ibm", "hexaware", "hr", "education"]
    },
    {
        "q": "Why did you choose AI and Machine Learning as your specialization?",
        "cat": "HR",
        "sub": "Domain Specialization",
        "d": "Beginner",
        "type": "hr",
        "roles": ["AI Engineer", "Machine Learning Engineer", "Data Scientist"],
        "stages": ["HR", "Technical Screening"],
        "ans": "Interviewers want to see genuine intellectual curiosity and practical grounding rather than chasing hype. Key points: 1) Data-driven shift: traditional programming requires explicit rules, whereas ML enables systems to learn complex patterns directly from historical data, 2) Practical curiosity: wanting to solve unstructured problems like computer vision, natural language understanding, and predictive analytics, 3) Real-world applications: seeing how AI enhances healthcare diagnosis, fraud detection, and recommendation engines, and 4) Hands-on validation: discovering the thrill of training models, evaluating metrics, and mitigating bias. Illustrative example: 'Traditional algorithms require hardcoding every edge case, which breaks down on complex real-world data like images or natural language. I chose AI and Machine Learning because I wanted to build systems that learn from empirical data and generalize to unseen scenarios. Building my first classifier and observing it correctly identify patterns that were impossible to manually code convinced me that intelligent automation is the future of software engineering.'",
        "kp": ["Distinguish rule-based software from data-driven pattern recognition", "Highlight curiosity for unstructured data problems (NLP, vision, tabular prediction)", "Connect specialization to hands-on model training and evaluation experience"],
        "crit": ["Clear, sound technical reasoning behind specialization choice", "Demonstrated awareness of real ML capabilities versus superficial sci-fi tropes"],
        "cm": ["Using science fiction cliches like 'I want to build a sentient robot'", "Inability to explain what machine learning actually does"],
        "fu": ["What is the biggest misconception non-technical people have about AI?", "How do you stay updated with research breakthroughs in LLMs?"],
        "tags": ["master-bank", "payoda", "sws-ai", "ibm", "hr", "ai-motivation", "top-30"]
    },
    {
        "q": "How would you describe your transition from school to college, and how have your academic marks changed?",
        "cat": "HR",
        "sub": "Self-Reflection & Growth",
        "d": "Intermediate",
        "type": "hr",
        "roles": ["Software Development Engineer", "AI Engineer"],
        "stages": ["HR"],
        "ans": "Interviewers use this question to evaluate self-awareness, honesty, resilience, and whether you take accountability for performance variations. School is typically heavily rote-memorization and rigid supervision; engineering college requires self-directed learning, independent research, lab execution, and balancing projects with theory. If your marks dipped: acknowledge the initial adjustment to open-ended engineering coursework, explain the specific corrective steps you took (forming study groups, prioritizing time, focusing on practical labs), and emphasize how your hands-on coding skills matured. If marks remained high or improved: highlight discipline, consistent study schedules, and applying classroom theory to practical software development.",
        "kp": ["Accountability without making excuses or blaming professors", "Contrast rote schooling with autonomous, application-driven engineering education", "Demonstrate continuous improvement and mastery of core technical skills"],
        "crit": ["Mature, non-defensive explanation of academic trajectory", "Concrete evidence of growth and engineering competence"],
        "cm": ["Blaming college faculty, tough grading, or attendance policies", "Becoming defensive or lying about academic performance"],
        "fu": ["What was the most demanding semester you faced and how did you navigate it?", "How do you balance theoretical coursework with hands-on coding practice?"],
        "tags": ["master-bank", "hexaware", "hr", "academics"]
    },
    {
        "q": "What is your SWOT analysis regarding your professional preparation?",
        "cat": "HR",
        "sub": "Self-Awareness & SWOT",
        "d": "Intermediate",
        "type": "hr",
        "roles": ["Software Development Engineer", "AI Engineer", "Data Analyst"],
        "stages": ["HR", "Managerial"],
        "ans": "A structured SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis demonstrates strategic self-awareness and maturity: 1) Strengths: Strong fundamentals in Python and SQL, disciplined analytical problem-solving, and rapid adaptability to new frameworks, 2) Weaknesses: Hesitancy when speaking to very large non-technical audiences, which I am actively addressing by presenting in college technical symposiums, 3) Opportunities: The rapid growth of cloud platforms and generative AI tools, allowing freshers to build full-stack intelligent applications faster than ever before, and 4) Threats: Fast technology obsolescence, which I mitigate by mastering durable core principles (data structures, system design, OOP) rather than just syntax trends. Illustrative example: 'Conducting a SWOT analysis helped me target my preparation. My key strength is building end-to-end prototypes using Python and databases. My recognized weakness was public presentation anxiety, which I worked on by leading our final year project demos. My biggest opportunity is leveraging modern AI developer tools to accelerate coding velocity, while my strategy against rapid tech obsolescence is continuously strengthening fundamental algorithms and clean code practices.'",
        "kp": ["Cover all 4 quadrants clearly: Strengths, Weaknesses, Opportunities, Threats", "Provide actionable mitigation strategies for identified weaknesses and threats", "Tie attributes directly to software engineering readiness"],
        "crit": ["Analytical, honest self-assessment without arrogance or false modesty", "Demonstrated action plan for personal and technical growth"],
        "cm": ["Listing fake weaknesses like 'I work too hard'", "Presenting threats without any proactive mitigation plan"],
        "fu": ["How has addressing your weakness improved your project teamwork?", "Which opportunity do you intend to focus on in your first year of employment?"],
        "tags": ["master-bank", "hexaware", "hr", "swot", "self-awareness"]
    },
    {
        "q": "What are your short-term and long-term goals?",
        "cat": "HR",
        "sub": "Career Goals",
        "d": "Beginner",
        "type": "hr",
        "roles": ["Software Development Engineer", "AI Engineer", "Java Developer"],
        "stages": ["HR", "Final"],
        "ans": "Interviewers assess whether you have realistic career ambitions, long-term commitment, and clarity of direction. Framework: 1) Short-term goal (0–2 years): Seamlessly onboard into the production codebase, master enterprise engineering practices (version control, CI/CD, testing, code reviews), earn the trust of senior developers, and become an independent contributor delivering high-quality user features. 2) Long-term goal (3–5 years): Deepen domain expertise in system architecture and cloud infrastructure, mentor junior engineers, take ownership of end-to-end module lifecycles, and contribute to architectural decisions that drive business growth. Illustrative example: 'In the short term, my goal is to join an engineering team where I can contribute to production-grade applications, master the company's tech stack, and deliver clean, tested code. In the long term over the next 3 to 5 years, I see myself growing into a senior software engineer or technical module lead, taking ownership of scalable system architectures and guiding new engineers.'",
        "kp": ["Realistic, grounded 1-2 year goals focused on learning, delivery, and team trust", "Forward-looking 3-5 year goals focused on architecture, mentorship, and ownership", "Alignment between your personal ambition and the company's growth"],
        "crit": ["Clear distinction between short-term and long-term milestones", "Plausible timeline demonstrating focus on engineering mastery"],
        "cm": ["Saying 'I want to start my own company in 1 year' or 'I want to do an MBA next fall'", "Vague answers like 'I just want to be successful'"],
        "fu": ["What specific technical skill are you currently learning to meet your short-term goal?", "How will you measure whether you achieved your 2-year objective?"],
        "tags": ["master-bank", "ibm", "hexaware", "payoda", "hr", "goals", "top-30"]
    },
    {
        "q": "What would you do if your manager did not like you or did not value your ideas?",
        "cat": "Company & Workplace",
        "sub": "Workplace Conflict & Hierarchy",
        "d": "Intermediate",
        "type": "hr",
        "roles": ["Software Development Engineer", "AI Engineer"],
        "stages": ["HR", "Managerial"],
        "ans": "Interviewers test emotional intelligence, professional detachment, resilience, and maturity in workplace relationships. Key strategy: 1) Separate personal perception from professional execution: personal affinity is secondary; delivering reliable, high-quality work is paramount, 2) Seek objective feedback: schedule a 1-on-1 meeting and ask clarifying questions like 'What specific outcomes or metrics can I focus on to better align with your expectations?', 3) Improve idea pitch quality: understand that managers reject ideas that lack concrete business data, risk assessments, or implementation feasibility; present ideas backed by data and prototypes rather than emotional opinions, 4) Practice patience and consistency: earn technical credibility through small wins before expecting buy-in on major architectural changes. Illustrative example: 'If I sensed friction, I would not take it personally. I would schedule a 1-on-1 to ask for constructive feedback on my work output. If my ideas weren't being adopted, I would reflect on whether I presented them with sufficient data, ROI metrics, and proof-of-concept testing. My priority would always be delivering on core team sprint deliverables while continuously improving how I communicate value.'",
        "kp": ["Emotional stability and professional objectivity over emotional retaliation", "Proactive 1-on-1 communication seeking actionable performance feedback", "Backing technical ideas with metrics, data, and prototypes rather than pride"],
        "crit": ["High emotional intelligence and constructive conflict resolution", "Commitment to team outcomes and manager alignment"],
        "cm": ["Saying 'I would complain to HR or the CEO immediately'", "Displaying resentment, passive aggressiveness, or work slowdown"],
        "fu": ["Have you ever had a disagreement with a project teammate, and how did you resolve it?", "How do you distinguish constructive technical criticism from personal bias?"],
        "tags": ["master-bank", "hexaware", "company-workplace", "conflict-resolution", "managerial"]
    },
    {
        "q": "What would you do if the company did not give you a salary hike for four years?",
        "cat": "Company & Workplace",
        "sub": "Compensation & Career Patience",
        "d": "Advanced",
        "type": "hr",
        "roles": ["Software Development Engineer", "AI Engineer"],
        "stages": ["HR", "Managerial"],
        "ans": "This is a stress-testing question designed to examine your patience, business awareness, assertiveness, and professional communication regarding compensation. Best approach: 1) Understand corporate context: evaluate if company-wide financial freezes or market downturns caused the freeze, 2) Perform honest self-evaluation: review whether your responsibilities, scope, and technical output actually expanded beyond an entry-level fresher over those years, 3) Prepare a data-backed business case: document your contributions, revenue impact, tickets resolved, and leadership in sprint reviews, 4) Schedule a professional appraisal discussion: present your achievements to your manager and ask for clear, measurable milestones required to qualify for promotion and salary revision, and 5) Make a dignified, objective career evaluation: if company growth or budget no longer aligns with your career trajectory despite consistent high performance, explore internal transfers or external career progression professionally without burning bridges.",
        "kp": ["Objective, calm demeanor without anger or entitlement", "Evaluate business macroeconomic context alongside personal performance", "Build a verifiable brag sheet of achievements and business impact", "Professional milestone alignment with manager before making career decisions"],
        "crit": ["Mature, pragmatic approach to compensation discussions", "Focus on value creation before compensation demands"],
        "cm": ["Saying 'I would quit immediately on day one' or 'I would leak company code'", "Saying 'I would work without complaint forever' (unrealistic and subservient)"],
        "fu": ["How do you track your personal productivity and value in a software team?", "What matters more to you in your first two years: learning curve or immediate compensation?"],
        "tags": ["master-bank", "hexaware", "company-workplace", "compensation", "professionalism"]
    },
    {
        "q": "Will AI replace software engineers, and if AI can write code, why do we need software engineers?",
        "cat": "Company & Workplace",
        "sub": "AI Impact & Engineering Role",
        "d": "Intermediate",
        "type": "hr",
        "roles": ["Software Development Engineer", "AI Engineer", "Full-Stack Developer"],
        "stages": ["HR", "Technical Screening", "Final"],
        "ans": "This question tests your philosophical and technical understanding of software engineering beyond mere syntax typing. Key insights: 1) Syntax generation vs. system engineering: Writing code syntax is only 20% of engineering; 80% is understanding ambiguous customer requirements, system architecture, trade-off analysis, security posture, and domain logic, 2) AI as a cognitive amplifier: AI tools (Copilot, LLMs) automate boilerplate code, regex, and repetitive unit tests, allowing engineers to operate at a higher level of abstraction—just like compilers replaced punch cards and high-level languages replaced assembly, 3) Accountability and edge cases: LLMs cannot take legal, ethical, or architectural accountability for catastrophic system failures, data privacy leaks, or subtle race conditions, 4) The engineer as the orchestrator: The engineer of the future is an architect and verifier who designs prompt pipelines, reviews AI-generated logic for security, and integrates multi-system architectures. Illustrative example: 'AI will not replace software engineers, but engineers who effectively leverage AI will replace those who don't. Writing syntax is just the implementation detail; the true value of an engineer lies in problem formulation, translating ambiguous business needs into resilient system architectures, verifying edge cases, and ensuring production security and reliability.'",
        "kp": ["Distinguish code typing from holistic system engineering and problem formulation", "Analogize AI code assistants to historical developer productivity leaps (compilers, cloud)", "Highlight the indispensable role of engineers in verification, edge cases, and architecture", "Frame AI as a force multiplier that elevates engineer productivity"],
        "crit": ["Nuanced, technically literate perspective avoiding extreme alarmism or denial", "Articulation of the evolving role of software engineers in the AI era"],
        "cm": ["Saying 'Yes, software engineering is dead, nobody should learn coding'", "Saying 'No, AI is completely useless and will never write good code'"],
        "fu": ["How have you used AI developer tools in your own project workflows?", "What are the key security and hallucination risks of copy-pasting AI code into production?"],
        "tags": ["master-bank", "hexaware", "ibm", "sws-ai", "ai-impact", "philosophy", "top-30"]
    },

    # -------------------------------------------------------------
    # PART 2: RESUME, PROJECTS, AND INTERNSHIP QUESTIONS
    # -------------------------------------------------------------
    {
        "q": "Explain your project architecture and the complete workflow from user request to database.",
        "cat": "Resume & Projects",
        "sub": "Project Architecture & Workflow",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["Software Development Engineer", "Full-Stack Developer", "AI Engineer"],
        "stages": ["Technical", "Final"],
        "ans": "Interviewers use this to verify whether you actually built the project or just downloaded a tutorial repository. Structure your answer across the complete end-to-end stack: 1) Client Layer: React/Vite single-page application captures user input, manages form state with React hooks, and issues an asynchronous HTTP request (e.g., via Axios/Fetch) with JWT authentication headers, 2) API Gateway / Backend: FastAPI or Express receives the request, passes it through CORS and authentication middleware, validates the payload using Pydantic schemas, and routes it to the controller, 3) Business / Processing Layer: Controller executes business logic, invokes algorithms or AI model inference pipelines, and handles error boundaries, 4) Persistence Layer: Database client (SQLAlchemy or Supabase PostgreSQL client) queries or updates the database via connection pooling, and 5) Response Pipeline: The formatted JSON response returns through HTTP status codes (200 OK, 201 Created) to update the client UI optimistically. Illustrative example: 'In my project, when a user uploads a document, the React frontend sends a multipart form request to a FastAPI endpoint. The backend validates the file type, stores the raw binary in cloud storage, and queues a background worker to extract text, generate vector embeddings, and store embeddings in PostgreSQL with pgvector. The endpoint returns a 202 Accepted status with a job ID, allowing the frontend to poll or listen for completion.'",
        "kp": ["Trace the request step-by-step: Client -> Network -> Gateway -> Service Layer -> DB -> Response", "Specify concrete protocols, validation mechanisms, and status codes", "Demonstrate clear mental models of separation of concerns in modern architectures"],
        "crit": ["Technical depth and fluency when describing data movement across layers", "Clear ownership of architectural design decisions"],
        "cm": ["Saying 'It just works automatically' without explaining middleware or serialization", "Inability to name the database ORM, API framework, or communication protocol"],
        "fu": ["What happens if the database connection drops while the user is submitting data?", "How do you handle authentication tokens across frontend reloads?"],
        "tags": ["master-bank", "ibm", "aquaairx", "payoda", "sws-ai", "wheelson", "architecture", "top-30"]
    },
    {
        "q": "What challenges did you face during development, and how did you solve those challenges?",
        "cat": "Resume & Projects",
        "sub": "Problem Solving & Debugging",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["Software Development Engineer", "AI Engineer", "Full-Stack Developer"],
        "stages": ["Technical", "Final"],
        "ans": "A strong technical challenge answer follows the STAR framework (Situation, Task, Action, Result) with specific engineering depth: 1) The technical bottleneck: Explain the concrete bug, performance bottleneck, or integration breakdown (e.g., API CORS issues, memory leak during large dataset preprocessing, slow DB query latency, or model overfitting), 2) Systematic diagnosis: Explain how you investigated the root cause using browser network tabs, server logs, profiling tools, or isolated unit tests rather than random guessing, 3) Engineering resolution: Explain the architectural or code-level fix implemented (e.g., adding database indexing, implementing batch processing with generators, configuring proper CORS headers, or applying L2 regularization), and 4) Measurable outcome: Quantify the improvement (e.g., query execution dropped from 1.8s to 45ms, memory consumption dropped by 70%). Illustrative example: 'During our AI document processing project, batch inference crashed the server with Out-Of-Memory (OOM) errors whenever users uploaded files larger than 50MB. I profiled the server and realized our endpoint was loading entire files into memory simultaneously. I refactored the ingestion pipeline to stream file chunks and process embeddings using Python generators in batches of 32. This reduced peak RAM consumption by 75% and enabled seamless processing of 200MB files.'",
        "kp": ["STAR format: Context -> Specific Engineering Bottleneck -> Diagnostic Method -> Measurable Fix", "Demonstrate disciplined debugging using profiling, logging, and metrics", "Quantify the before-and-after performance improvement"],
        "crit": ["Authentic technical problem solving rather than trivial syntax typos", "Clear articulation of trade-offs and root-cause analysis"],
        "cm": ["Saying 'I had no challenges, everything was smooth'", "Mentioning trivial issues like 'I forgot a semicolon' as your biggest challenge"],
        "fu": ["How did you verify that your fix didn't introduce regression bugs?", "What would you do differently if you re-architected that module today?"],
        "tags": ["master-bank", "ibm", "payoda", "aquaairx", "sws-ai", "debugging", "top-30"]
    },
    {
        "q": "How would you deploy your project and scale it if it received a large number of users?",
        "cat": "Resume & Projects",
        "sub": "Deployment & Scalability",
        "d": "Advanced",
        "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Full-Stack Developer", "AI Engineer"],
        "stages": ["Technical", "Final"],
        "ans": "This question evaluates architectural maturity and readiness for production cloud environments. Scaling strategy: 1) Containerization & Hosting: Package the application into Docker containers to guarantee environment parity across staging and production, hosted on cloud container services (AWS ECS, Google Cloud Run, or Kubernetes), 2) Stateless Backend & Horizontal Scaling: Keep the backend API stateless so incoming traffic can be distributed across multiple container instances via an Application Load Balancer (ALB) or Nginx reverse proxy, 3) Caching Layer: Introduce Redis to cache frequent read queries (e.g., user profiles, catalog items, popular search results) and reduce database load, 4) Database Scaling: Implement connection pooling (PgBouncer), read replicas to separate read-heavy traffic from writes, and proper column indexing, 5) Asynchronous Task Queues: Offload heavy tasks (email notifications, AI inference, document conversion) to background worker queues using Celery or Redis Queue with message brokers (RabbitMQ/Redis), 6) CDN & Static Assets: Serve frontend static bundles and media via Cloudflare or AWS CloudFront CDN for sub-50ms latency globally.",
        "kp": ["Docker containerization for consistent deployment environments", "Stateless horizontal scaling behind a load balancer", "Redis caching to eliminate redundant database read queries", "Background worker queues (Celery/Redis) for asynchronous heavy lifting", "Database connection pooling and read replicas"],
        "crit": ["Systemic understanding of scalability bottlenecks beyond single-machine limits", "Clear articulation of caching, load balancing, and async queues"],
        "cm": ["Saying 'I would just buy a bigger server' (vertical scaling only)", "Forgetting database connection limits when spawning multiple backend instances"],
        "fu": ["How do you handle database write contention under high concurrency?", "What is the difference between horizontal and vertical scaling?"],
        "tags": ["master-bank", "ibm", "sws-ai", "wheelson", "deployment", "scalability"]
    },
    {
        "q": "How did you prevent overfitting in your machine learning project?",
        "cat": "ML, AI & GenAI",
        "sub": "Model Generalization",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["Machine Learning Engineer", "AI Engineer", "Data Scientist"],
        "stages": ["Technical"],
        "ans": "Overfitting occurs when an ML model memorizes noise and specific patterns in the training data rather than learning generalizable underlying relationships, resulting in near-perfect training accuracy but poor validation/test performance. Engineering techniques to prevent overfitting: 1) Cross-Validation: Use K-Fold stratified cross-validation to ensure model performance is consistent across different data subsets, 2) Data Augmentation & Gathering: Increase training diversity using techniques like synthetic noise, random rotations/crops (for images), or back-translation (for text), 3) Regularization: Apply L1 (Lasso, driving redundant weights to zero) or L2 (Ridge, penalizing large weights) regularization to constrain model complexity, 4) Dropout & Early Stopping (Deep Learning): Randomly deactivate neurons during training (e.g., 20-50% dropout) and halt training when validation loss stops improving for a specified patience window, 5) Tree Pruning & Constraining (Tree Models): Set max_depth, min_samples_split, and min_samples_leaf in Random Forest or XGBoost to prevent overly deep, hyper-specific decision branches.",
        "kp": ["Define overfitting clearly: high training performance, degraded test/validation performance (high variance)", "Apply structural constraints: L1/L2 regularization, tree depth limits, and dropout", "Implement robust validation protocols: K-fold cross-validation and early stopping"],
        "crit": ["Solid grasp of bias-variance trade-off and generalization mechanics", "Specific references to hyperparameters configured in personal projects"],
        "cm": ["Confusing overfitting with underfitting", "Claiming 100% test accuracy without realizing it indicates data leakage or severe overfitting"],
        "fu": ["What is data leakage and how do you prevent it during feature scaling?", "How does early stopping determine when to halt training epochs?"],
        "tags": ["master-bank", "payoda", "sws-ai", "ibm", "machine-learning", "overfitting", "top-30"]
    },
    {
        "q": "Tell me about your internship: what were your responsibilities and what did you learn?",
        "cat": "Resume & Projects",
        "sub": "Internship Experience",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["Software Development Engineer", "AI Engineer", "Data Analyst"],
        "stages": ["Technical", "HR", "Final"],
        "ans": "Interviewers evaluate your transition from academic theory to corporate software engineering environments. Structure: 1) Company context & team: Name of organization, duration, and the team's charter, 2) Individual responsibilities: Specific modules or tickets you owned (e.g., building REST API endpoints, redesigning responsive UI components, optimizing database queries, or automating test scripts), 3) Technical toolchain: Experience with enterprise tools (Git branching, Jira sprint tracking, Docker, code reviews), 4) Key engineering challenge & resolution: A concrete deliverable you pushed to staging/production, and 5) Key takeaways: Learning how to read unfamiliar codebases, communicate blockers early, and adhere to clean code standards. Illustrative example: 'During my 3-month internship at a software consultancy, I worked as a backend developer intern. My core responsibility was developing RESTful microservices for user notification and audit logging using Python and PostgreSQL. I participated in daily standups, raised pull requests reviewed by senior engineers, and wrote PyTest unit tests achieving 85% test coverage. My biggest learning was understanding how professional codebases prioritize maintainability, structured logging, and edge-case validation over quick-and-dirty scripting.'",
        "kp": ["Differentiate academic coding from professional enterprise engineering standards", "Highlight individual contribution, code reviews, and version control discipline", "Demonstrate maturity in communicating blockers and collaborating with senior peers"],
        "crit": ["Credible, detailed description of tasks and team interactions", "Clear articulation of professional growth and engineering habits formed"],
        "cm": ["Vague summaries like 'I attended meetings and observed people'", "Claiming you single-handedly built the company's entire flagship product"],
        "fu": ["What was the most constructive piece of feedback you received in a code review?", "How did your internship project differ from your academic college projects?"],
        "tags": ["master-bank", "ibm", "hexaware", "aquaairx", "internship", "experience"]
    },

    # -------------------------------------------------------------
    # PART 3: PROGRAMMING AND CODING QUESTIONS
    # -------------------------------------------------------------
    {
        "q": "Write a program to check whether a string is a palindrome.",
        "cat": "Coding",
        "sub": "String Algorithms",
        "d": "Beginner",
        "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "A palindrome is a string that reads the same forwards and backwards, ignoring non-alphanumeric characters and casing if specified. Optimized Approach: Two-Pointer Technique (Time: O(N), Space: O(1)). We initialize two pointers: `left` at index 0 and `right` at index len(s) - 1. While `left < right`, we compare the characters at both pointers. If they match, advance `left` and decrement `right`; if they don't match, return False. If pointers cross, return True. Python Code:\n```python\ndef is_palindrome(s: str) -> bool:\n    # Clean and normalize if alphanumeric validation is requested\n    cleaned = [c.lower() for c in s if c.isalnum()]\n    left, right = 0, len(cleaned) - 1\n    while left < right:\n        if cleaned[left] != cleaned[right]:\n            return False\n        left += 1\n        right -= 1\n    return True\n\n# Quick one-liner (O(N) space):\ndef is_palindrome_simple(s: str) -> bool:\n    return s == s[::-1]\n```\nTime Complexity: O(N) where N is string length. Space Complexity: O(1) for in-place pointer checking on an alphanumeric string, or O(N) for string slicing.",
        "kp": ["Two-pointer approach operates in O(N) time and O(1) auxiliary space", "Clarify with interviewer whether non-alphanumeric characters and casing should be ignored", "Explain trade-off between memory-efficient two pointers vs concise slice s[::-1]"],
        "crit": ["Correct algorithmic implementation handling edge cases (empty string, single char, spaces)", "Clear explanation of time and space complexity"],
        "cm": ["Failing to handle case sensitivity (e.g., 'Racecar' should often evaluate to true)", "Using inefficient O(N^2) string concatenations in a reverse loop"],
        "fu": ["How would you check if a string is a palindrome by removing at most one character (Valid Palindrome II)?", "What is the space complexity of s[::-1] in Python?"],
        "tags": ["master-bank", "ibm", "aquaairx", "hexaware", "coding", "strings", "palindrome", "top-30"]
    },
    {
        "q": "Count the vowels in a string, and count each vowel separately.",
        "cat": "Coding",
        "sub": "String Algorithms",
        "d": "Beginner",
        "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Problem: Count total vowels ('a', 'e', 'i', 'o', 'u') and maintain an individual tally for each vowel. Algorithm: 1) Initialize a dictionary or fixed-size frequency array for vowels: {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}, 2) Iterate through each character in the string, convert to lowercase, 3) If character is in the vowel set, increment its dictionary counter, 4) Sum the dictionary values for total vowel count. Python Code:\n```python\ndef count_vowels_detailed(text: str) -> tuple[int, dict[str, int]]:\n    vowel_counts = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}\n    total_vowels = 0\n    for char in text.lower():\n        if char in vowel_counts:\n            vowel_counts[char] += 1\n            total_vowels += 1\n    return total_vowels, vowel_counts\n\n# Example usage:\ntotal, breakdown = count_vowels_detailed('InterviewAce Master Question Bank')\nprint(f'Total: {total}, Breakdown: {breakdown}')\n```\nTime Complexity: O(N) single pass over the string. Space Complexity: O(1) since vowel dictionary is fixed at 5 keys.",
        "kp": ["Single pass linear scan O(N) over input string", "Use hash map / dictionary for O(1) vowel lookups and frequency tracking", "Handle case normalization (upper and lowercase vowels)"],
        "crit": ["Clean, bug-free implementation returning both total and individual tallies", "Proper time and space complexity analysis"],
        "cm": ["Forgetting uppercase vowels ('A', 'E', 'I', 'O', 'U')", "Writing nested loops resulting in O(N*5) instead of O(1) lookup"],
        "fu": ["How would you find the first vowel that appears in the string?", "What data structure would you use in Java or C++ instead of a dictionary?"],
        "tags": ["master-bank", "ibm", "aquaairx", "coding", "strings", "vowels", "top-30"]
    },
    {
        "q": "Generate the Fibonacci sequence up to N terms, and explain both iterative and recursive approaches.",
        "cat": "Coding",
        "sub": "Number Algorithms & Recursion",
        "d": "Beginner",
        "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "The Fibonacci sequence starts with 0 and 1, where each subsequent number is the sum of the previous two: F(n) = F(n-1) + F(n-2). Approaches: 1) Iterative (Preferred in production): Uses two variables `a` and `b`. Time: O(N), Space: O(1). 2) Naive Recursion: Repeatedly computes subproblems in an exponential call tree. Time: O(2^N), Space: O(N) call stack. 3) Memoized Recursion / Dynamic Programming: Caches computed Fibonacci numbers. Time: O(N), Space: O(N). Python Implementation:\n```python\n# Iterative approach (O(N) time, O(1) auxiliary space)\ndef fibonacci_iterative(n: int) -> list[int]:\n    if n <= 0: return []\n    if n == 1: return [0]\n    seq = [0, 1]\n    a, b = 0, 1\n    for _ in range(2, n):\n        c = a + b\n        seq.append(c)\n        a, b = b, c\n    return seq\n\n# Recursive with memoization\nfrom functools import lru_cache\n@lru_cache(maxsize=None)\ndef fib_memo(n: int) -> int:\n    if n < 0: raise ValueError('Positive integers only')\n    if n <= 1: return n\n    return fib_memo(n - 1) + fib_memo(n - 2)\n```\nInterviewers look for your ability to explain why naive recursion causes stack overflow and exponential redundant computations.",
        "kp": ["Iterative solution runs in O(N) time and O(1) space", "Naive recursion suffers from O(2^N) exponential time complexity due to overlapping subproblems", "Memoization / DP reduces recursive time complexity to linear O(N)"],
        "crit": ["Clean implementation of iterative sequence generation", "Clear theoretical explanation of call stack depth and memoization"],
        "cm": ["Presenting naive recursion without mentioning its exponential time complexity", "Off-by-one errors in sequence length or zero-indexing"],
        "fu": ["How would you compute the N-th Fibonacci number in O(log N) time using matrix exponentiation?", "What happens to the Python call stack if you call fib_recursive(1000)?"],
        "tags": ["master-bank", "ibm", "aquaairx", "coding", "numbers", "fibonacci", "recursion", "top-30"]
    },
    {
        "q": "Check whether a number is prime, and print all prime numbers within a given range.",
        "cat": "Coding",
        "sub": "Mathematical Algorithms",
        "d": "Beginner",
        "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "A prime number is an integer greater than 1 that has no positive divisors other than 1 and itself. Optimization: Factors always appear in pairs (a * b = N). At least one factor must be <= sqrt(N). Hence, testing divisibility up to int(sqrt(N)) is sufficient: O(sqrt(N)) time. For range generation, the Sieve of Eratosthenes is optimal: O(N log log N) time. Python Implementation:\n```python\nimport math\n\ndef is_prime(n: int) -> bool:\n    if n <= 1:\n        return False\n    if n <= 3:\n        return True\n    if n % 2 == 0 or n % 3 == 0:\n        return False\n    # Check up to sqrt(n) with 6k +/- 1 step\n    i = 5\n    while i * i <= n:\n        if n % i == 0 or n % (i + 2) == 0:\n            return False\n        i += 6\n    return True\n\ndef primes_in_range(start: int, end: int) -> list[int]:\n    return [num for num in range(max(2, start), end + 1) if is_prime(num)]\n```\nTime Complexity: `is_prime` runs in O(sqrt(N)). For printing primes up to M, Sieve of Eratosthenes achieves O(M log log M).",
        "kp": ["Check divisibility only up to int(sqrt(N)) rather than N", "Handle base cases cleanly: n <= 1 is not prime, 2 and 3 are prime", "Understand the Sieve of Eratosthenes for generating primes across large ranges"],
        "crit": ["Optimized sqrt(N) implementation instead of naive O(N) loop", "Accurate handling of negative numbers, 0, 1, and even numbers"],
        "cm": ["Checking numbers all the way up to N-1 (inefficient O(N))", "Considering 1 or 0 as prime numbers"],
        "fu": ["What is the time complexity of the Sieve of Eratosthenes?", "How does trial division compare to probabilistic primality tests like Miller-Rabin for 512-bit primes?"],
        "tags": ["master-bank", "ibm", "aquaairx", "coding", "primes", "math", "top-30"]
    },
    {
        "q": "Find the second-largest element in an array without sorting.",
        "cat": "Coding",
        "sub": "Array Algorithms",
        "d": "Beginner",
        "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Sorting the array takes O(N log N) time. The optimal approach finds the second-largest element in a single pass O(N) with O(1) space. Algorithm: 1) Initialize `first` and `second` to negative infinity (`float('-inf')`), 2) Traverse each number `x` in the array: If `x > first`: update `second = first`, then `first = x`. Else if `x > second` and `x != first`: update `second = x`, 3) If `second` remains negative infinity (e.g., all array elements are identical or array length < 2), return None. Python Implementation:\n```python\ndef find_second_largest(arr: list[int]) -> int | None:\n    if len(arr) < 2:\n        return None\n    first = second = float('-inf')\n    for x in arr:\n        if x > first:\n            second = first\n            first = x\n        elif x > second and x != first:\n            second = x\n    return second if second != float('-inf') else None\n\n# Example: [12, 35, 1, 10, 34, 1] -> 34\n```\nTime Complexity: O(N) single pass. Space Complexity: O(1) auxiliary variables.",
        "kp": ["Single pass O(N) traversal without using O(N log N) sorting", "Track both first and second largest simultaneously", "Properly handle duplicate maximums (e.g., [10, 10, 10] has no distinct second largest)"],
        "crit": ["Single traversal O(N) time and O(1) space", "Correct handling of duplicates, negative numbers, and arrays with < 2 elements"],
        "cm": ["Using arr.sort() and returning arr[-2] (fails when duplicate maximums exist like [10, 10, 8])", "Assuming all numbers in the array are positive"],
        "fu": ["How would you find the K-th largest element in an array in O(N) average time (Quickselect or Min-Heap)?", "What if the input stream is continuous and infinite?"],
        "tags": ["master-bank", "ibm", "aquaairx", "coding", "arrays", "second-largest", "top-30"]
    },
    {
        "q": "Move all zeros to the end of an array while maintaining the relative order of non-zero elements.",
        "cat": "Coding",
        "sub": "Array Algorithms & In-Place",
        "d": "Beginner",
        "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Problem: Given an integer array, move all 0's to the end while maintaining the relative order of non-zero elements in-place: O(N) time and O(1) space. Two-Pointer In-Place Technique: 1) Maintain a pointer `non_zero_idx = 0` representing the index where the next non-zero element should be placed, 2) Iterate pointer `curr` from index 0 to len(arr) - 1, 3) Whenever `arr[curr] != 0`, swap `arr[non_zero_idx]` with `arr[curr]` and increment `non_zero_idx`. Python Implementation:\n```python\ndef move_zeros_to_end(arr: list[int]) -> list[int]:\n    non_zero_idx = 0\n    for curr in range(len(arr)):\n        if arr[curr] != 0:\n            # Swap non-zero element to the front\n            arr[non_zero_idx], arr[curr] = arr[curr], arr[non_zero_idx]\n            non_zero_idx += 1\n    return arr\n\n# Example: [0, 1, 0, 3, 12] -> [1, 3, 12, 0, 0]\n```\nTime Complexity: O(N) single traversal. Space Complexity: O(1) in-place modification.",
        "kp": ["In-place swap algorithm avoids allocating O(N) temporary array", "Maintains relative order of non-zero numbers", "Runs in single pass O(N) time"],
        "crit": ["Clean in-place logic without extra list allocations", "Correct execution on arrays with all zeros, no zeros, or alternating zeros"],
        "cm": ["Allocating a new list and using append() (violates in-place requirement)", "Using arr.remove(0) in a loop, which causes O(N^2) shifting"],
        "fu": ["How many total write operations does this swap approach perform?", "What is the difference between this problem and the Dutch National Flag partitioning?"],
        "tags": ["master-bank", "ibm", "aquaairx", "coding", "arrays", "two-pointers", "top-30"]
    },

    # -------------------------------------------------------------
    # PART 4: PYTHON INTERVIEW QUESTIONS
    # -------------------------------------------------------------
    {
        "q": "What is the difference between a list, tuple, set, and dictionary in Python?",
        "cat": "Python",
        "sub": "Core Data Structures",
        "d": "Beginner",
        "type": "technical",
        "roles": ["Python Developer", "Software Development Engineer", "AI Engineer", "Data Analyst"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Python's four built-in collection data structures differ in mutability, ordering, uniqueness, and internal implementation: 1) List (`[]`): Ordered, mutable collection that allows duplicate elements. Implemented as a dynamic array with O(1) amortized append and O(1) index access. 2) Tuple (`()`): Ordered, immutable collection that allows duplicates. Memory-efficient, faster than lists, and can be used as dictionary keys if all contents are hashable. 3) Set (`{}`): Unordered collection of unique, hashable elements. Implemented via a hash table with O(1) average lookup, insertion, and deletion. Cannot contain mutable items like lists. 4) Dictionary (`{key: value}`): Ordered collection of key-value pairs (ordered since Python 3.7). Keys must be unique and immutable/hashable; values can be of any type. Implemented via a sparse hash table with O(1) average lookup.",
        "kp": ["List: ordered, mutable, duplicates allowed (dynamic array)", "Tuple: ordered, immutable, duplicates allowed (fixed memory buffer)", "Set: unordered/unique, hash-table backed, O(1) membership testing", "Dict: key-value mapping, unique hashable keys, O(1) key lookups"],
        "crit": ["Accurate comparison across all four structures regarding mutability, indexing, and duplicates", "Clear understanding of underlying hash tables vs dynamic arrays"],
        "cm": ["Stating that dictionaries are unordered in modern Python (ordered since 3.7)", "Claiming tuples can never contain mutable objects (a tuple can hold a mutable list)"],
        "fu": ["Can a list be used as a dictionary key or set element, and why not?", "What is the memory footprint difference between an empty list and an empty tuple?"],
        "tags": ["master-bank", "ibm", "aquaairx", "payoda", "python", "data-structures", "top-30"]
    },
    {
        "q": "What are *args and **kwargs in Python, and how are they used?",
        "cat": "Python",
        "sub": "Function Arguments",
        "d": "Beginner",
        "type": "technical",
        "roles": ["Python Developer", "Software Development Engineer", "AI Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "`*args` and `**kwargs` allow a function to accept a dynamic, arbitrary number of arguments: 1) `*args` (Positional variable arguments): The asterisk unpacks any positional arguments passed beyond the named parameters and packs them into a single `tuple`. 2) `**kwargs` (Keyword variable arguments): The double asterisk unpacks named keyword arguments and packs them into a single `dictionary`. 3) Argument Ordering Convention: Standard order in function definitions must be: `standard_args, *args, default_args, **kwargs`. Python Code:\n```python\ndef log_event(event_name, *tags, **metadata):\n    print(f'Event: {event_name}')\n    print(f'Tags tuple: {tags}')        # e.g., ('auth', 'security')\n    print(f'Metadata dict: {metadata}') # e.g., {'user_id': 101, 'ip': '127.0.0.1'}\n\nlog_event('user_login', 'auth', 'security', user_id=101, ip='127.0.0.1')\n```\nCommonly used in decorator wrappers, subclass method overriding (calling `super().__init__(*args, **kwargs)`), and creating flexible API handlers.",
        "kp": ["*args packs excess positional arguments into a tuple", "**kwargs packs excess keyword arguments into a dictionary", "Essential for decorator design patterns and extensible class inheritance"],
        "crit": ["Clear syntax and semantic distinction between single and double asterisk", "Understanding argument ordering rules in Python functions"],
        "cm": ["Believing the words 'args' and 'kwargs' are keywords (only the asterisks * and ** are syntactically required)", "Placing **kwargs before positional arguments in function signature"],
        "fu": ["How do you unpack a dictionary into function arguments when calling a function?", "What is keyword-only argument syntax introduced in Python 3?"],
        "tags": ["master-bank", "ibm", "python", "functions", "args-kwargs"]
    },
    {
        "q": "What is the difference between shallow copy and deep copy in Python?",
        "cat": "Python",
        "sub": "Object Mutation & Memory",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["Python Developer", "Software Development Engineer", "AI Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "When copying objects containing nested structures (e.g., a list of lists or dict of dicts): 1) Assignment (`b = a`): Does not create any copy; creates a new reference pointing to the exact same memory address (`b is a` is True). 2) Shallow Copy (`copy.copy(a)` or `a.copy()`): Constructs a new collection object, but inserts references to the original nested child objects. Modifying a nested mutable element in the copy also mutates the original object. 3) Deep Copy (`copy.deepcopy(a)`): Recursively constructs a brand-new collection and clones all child objects contained within it, decoupling the new structure entirely from the original. Python Code:\n```python\nimport copy\noriginal = [[1, 2, 3], [4, 5, 6]]\nshallow = copy.copy(original)\ndeep = copy.deepcopy(original)\n\n# Modifying nested element\nshallow[0][0] = 999\nprint(original[0][0])  # Prints 999! (Original was modified)\n\ndeep[1][0] = 888\nprint(original[1][0])  # Prints 4! (Original untouched)\n```",
        "kp": ["Assignment creates an alias reference without allocating new memory", "Shallow copy clones only the outer container; child references are shared", "Deep copy recursively clones all nested objects for complete isolation"],
        "crit": ["Clear code explanation showing nested mutation behavior", "Understanding when deep copy overhead is justified"],
        "cm": ["Assuming list slicing a[:] or a.copy() creates a deep copy (it only creates a shallow copy)", "Forgetting that deepcopy has performance and recursion overhead on large nested graphs"],
        "fu": ["How does copy.deepcopy handle cyclic references without infinite loops?", "What is the __copy__ and __deepcopy__ magic method protocol in custom classes?"],
        "tags": ["master-bank", "ibm", "aquaairx", "python", "memory", "copy"]
    },
    {
        "q": "What is the difference between an iterator and a generator in Python?",
        "cat": "Python",
        "sub": "Generators & Memory Optimization",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["Python Developer", "Software Development Engineer", "AI Engineer"],
        "stages": ["Technical", "Technical Screening"],
        "ans": "1) Iterator: An object that implements the iterator protocol with two methods: `__iter__()` (returns the iterator object itself) and `__next__()` (returns the next element or raises `StopIteration` when elements are exhausted). Iterators can be created manually by defining custom classes. 2) Generator: A simple, elegant way to create an iterator using a function containing the `yield` keyword, or using a generator expression `(x for x in data)`. 3) Lazy Evaluation: Generators produce items one at a time on demand instead of storing the entire sequence in memory simultaneously. A generator function saves its execution state (local variables, instruction pointer) across `yield` calls and resumes execution seamlessly when `next()` is invoked. 4) Memory Efficiency: Processing a 5GB file line-by-line using a generator uses only a few kilobytes of RAM, whereas reading `file.readlines()` loads all 5GB into memory at once.",
        "kp": ["Iterator protocol requires __iter__() and __next__() raising StopIteration", "Generators produce iterators automatically using the 'yield' keyword", "Lazy evaluation saves vast amounts of RAM when processing large streams"],
        "crit": ["Clear distinction between protocol implementation vs syntactic generator functions", "Emphasis on memory efficiency and execution state suspension"],
        "cm": ["Confusing yield with return (yield pauses execution; return terminates the function)", "Assuming generators can be rewound or indexed like lists"],
        "fu": ["What happens if you call next() on an exhausted generator?", "How can you pass values into a running generator using generator.send()?"],
        "tags": ["master-bank", "ibm", "payoda", "python", "generators", "iterators"]
    },
    {
        "q": "What is a decorator in Python, and how do you write a custom decorator?",
        "cat": "Python",
        "sub": "Metaprogramming & Decorators",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["Python Developer", "Software Development Engineer", "Backend Developer"],
        "stages": ["Technical"],
        "ans": "A decorator is a design pattern in Python that allows you to dynamically modify or extend the behavior of a function or class without permanently changing its source code. In Python, functions are first-class citizens, meaning they can be passed as arguments, returned from other functions, and assigned to variables. A decorator takes a target function as input, wraps it in an inner function that executes custom logic before and after calling the target, and returns the wrapper. Python Code:\n```python\nimport time\nfrom functools import wraps\n\ndef measure_time(func):\n    @wraps(func)  # Preserves target function's name and docstring\n    def wrapper(*args, **kwargs):\n        start = time.perf_counter()\n        result = func(*args, **kwargs)\n        elapsed = time.perf_counter() - start\n        print(f'{func.__name__} executed in {elapsed:.4f}s')\n        return result\n    return wrapper\n\n@measure_time\ndef process_records(n):\n    return sum(i * i for i in range(n))\n```\nUsed ubiquitously in FastAPI/Flask routing (`@app.get('/users')`), authentication (`@login_required`), rate limiting, and structured telemetry logging.",
        "kp": ["Decorators leverage first-class functions and closures", "Wrapper function uses *args, **kwargs to accept any signature", "@wraps(func) from functools preserves metadata (__name__, __doc__)", "Common use cases: logging, caching (@lru_cache), auth checks, route dispatching"],
        "crit": ["Correct implementation of outer closure and inner wrapper", "Explanation of why @functools.wraps is essential"],
        "cm": ["Forgetting to return the result of func(*args, **kwargs) from inside the wrapper", "Forgetting to return the wrapper function from the decorator"],
        "fu": ["How do you write a decorator that accepts arguments (decorator factory)?", "What is the execution order when multiple decorators are stacked on a function?"],
        "tags": ["master-bank", "ibm", "sws-ai", "wheelson", "python", "decorators"]
    },

    # -------------------------------------------------------------
    # PART 5: JAVA & OBJECT-ORIENTED PROGRAMMING QUESTIONS
    # -------------------------------------------------------------
    {
        "q": "What is the difference between JDK, JRE, and JVM in Java?",
        "cat": "Java & OOP",
        "sub": "Java Architecture",
        "d": "Beginner",
        "type": "technical",
        "roles": ["Software Development Engineer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Java's runtime architecture is divided into three concentric layers: 1) JVM (Java Virtual Machine): The abstract execution engine that interprets or JIT-compiles compiled `.class` bytecode into native machine instructions for the underlying operating system. It manages memory allocation, thread execution, and garbage collection. JVM is platform-dependent (different binaries for Windows, Linux, Mac), but provides Java's 'Write Once, Run Anywhere' (WORA) abstraction. 2) JRE (Java Runtime Environment): The runtime bundle needed to run compiled Java applications. It contains the JVM along with core Java standard libraries (rt.jar, util, lang) and supporting files. It has no developer tools (no compiler `javac`). 3) JDK (Java Development Kit): The complete software development package needed to write, compile, and run Java code. It includes the complete JRE plus developer tools such as the compiler (`javac`), debugger (`jdb`), archiver (`jar`), and documentation generator (`javadoc`). Hierarchy: JDK = JRE + Development Tools; JRE = JVM + Core Libraries.",
        "kp": ["JVM: executes bytecode, handles memory and garbage collection (platform-dependent)", "JRE: JVM + core runtime libraries for executing Java applications", "JDK: JRE + developer tools (javac compiler, debugger) for creating software"],
        "crit": ["Accurate structural hierarchy and purpose of each component", "Clear explanation of platform independence via bytecode and JVM"],
        "cm": ["Saying JVM is platform-independent (bytecode is independent; JVM implementations are OS-specific)", "Thinking JRE can compile Java source code"],
        "fu": ["What is the role of the JIT (Just-In-Time) compiler inside the JVM?", "What are the key memory areas managed by the JVM (Heap, Stack, Metaspace)?"],
        "tags": ["master-bank", "ibm", "aquaairx", "java", "jvm", "architecture", "top-30"]
    },
    {
        "q": "Explain the four pillars of Object-Oriented Programming with real-world software examples.",
        "cat": "Java & OOP",
        "sub": "OOP Fundamentals",
        "d": "Beginner",
        "type": "technical",
        "roles": ["Software Development Engineer", "Java Developer", "Python Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "The four pillars of OOP organize code into modular, reusable, and secure abstractions: 1) Encapsulation: Bundling data (state) and methods (behavior) into a single class unit while restricting direct external access to internal fields using private access modifiers, exposing safe getter and setter methods. Real-world example: A `BankAccount` class where `private double balance` cannot be mutated directly from outside; mutations must pass through `deposit()` and `withdraw()` with validation rules. 2) Abstraction: Hiding complex internal implementation details and exposing only the essential interface to the user. Real-world example: A TV remote button or an `interface PaymentGateway { void processPayment(double amount); }` where caller code calls `processPayment()` without knowing the complex banking network handshakes inside Stripe or PayPal. 3) Inheritance: The mechanism where a child subclass derives fields and behaviors from a parent superclass, promoting code reuse. Real-world example: `class ElectricCar extends Vehicle` inheriting `speed` and `brand` while adding `batteryCapacity`. 4) Polymorphism: The ability for an entity to take multiple forms—either Compile-Time (Method Overloading) or Runtime (Method Overriding via dynamic method dispatch). Real-world example: A base `Shape` class with a method `draw()`; `Circle` and `Square` override `draw()` with distinct renderings, and a list of shapes can all be drawn polymorphically via `shape.draw()`.",
        "kp": ["Encapsulation: data hiding with private fields and controlled getters/setters", "Abstraction: hiding implementation complexity behind clean interfaces", "Inheritance: code reuse via superclass and subclass relationships", "Polymorphism: method overloading (compile-time) and overriding (runtime)"],
        "crit": ["Accurate definition of all four pillars with distinct code examples", "Ability to explain practical software engineering benefits (maintainability, reusability)"],
        "cm": ["Confusing abstraction with encapsulation (encapsulation hides state; abstraction hides implementation complexity)", "Using vague non-software analogies without showing code mental models"],
        "fu": ["Why is composition often preferred over inheritance in modern software design?", "How does Java enforce abstraction using interfaces versus abstract classes?"],
        "tags": ["master-bank", "ibm", "aquaairx", "hexaware", "oop", "java", "top-30"]
    },
    {
        "q": "What is the difference between method overloading and method overriding?",
        "cat": "Java & OOP",
        "sub": "Polymorphism",
        "d": "Beginner",
        "type": "technical",
        "roles": ["Software Development Engineer", "Java Developer", "Python Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Overloading and Overriding represent the two distinct forms of polymorphism in object-oriented programming: 1) Method Overloading (Compile-Time / Static Polymorphism): Occurs within the SAME class. Multiple methods share the same name but differ in their parameter list (different number, types, or order of parameters). Return type alone cannot distinguish overloaded methods. Resolved at compile-time by the compiler based on argument types. Example: `add(int a, int b)` and `add(double a, double b)`. 2) Method Overriding (Runtime / Dynamic Polymorphism): Occurs between a SUPERCLASS and SUBCLASS. The subclass provides a specific implementation of a method that is already defined in its parent class. Method signature (name, parameter list, and compatible return type) must be identical. Resolved at runtime using dynamic method dispatch based on the actual object type created in heap memory. Example: `@Override public void makeSound()` in class `Dog` overriding `Animal.makeSound()`.",
        "kp": ["Overloading: same class, same method name, different parameter signature, resolved at compile-time", "Overriding: parent-child relationship, identical method signature, resolved at runtime via dynamic dispatch", "Overriding requires inheritance; overloading does not", "@Override annotation catches signature discrepancies at compile-time"],
        "crit": ["Clear, systematic comparison across class scope, signature rules, and binding time", "Demonstrates understanding of dynamic dispatch vs compile-time resolution"],
        "cm": ["Claiming changing only the return type creates a valid method overload (it causes a compiler error)", "Confusing static binding with dynamic binding"],
        "fu": ["Can you override private, static, or final methods in Java, and why not?", "What is covariant return type in method overriding?"],
        "tags": ["master-bank", "ibm", "aquaairx", "java", "oop", "polymorphism", "top-30"]
    },
    {
        "q": "Why is the Java String class immutable, and what is the difference between String, StringBuilder, and StringBuffer?",
        "cat": "Java & OOP",
        "sub": "String Internals",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["Software Development Engineer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "1) String Immutability: Once a `String` object is created in Java, its internal character array cannot be modified. Any modification creates a brand-new String object. Reasons for immutability: - String Constant Pool (SCP): Multiple string references with the same value share a single memory address in the pool, saving huge heap memory. - Thread Safety: Immutable objects can be freely shared across concurrent threads without synchronization locks. - Security: Strings store database URLs, usernames, passwords, and network sockets; if mutable, a malicious thread could alter a verified parameter. - Hashcode Caching: Because the contents never change, the hashcode is calculated once and cached, making Strings fast keys in HashMaps. 2) String vs StringBuilder vs StringBuffer: - `String`: Immutable; safe for sharing, but inefficient for repeated string concatenations in loops (allocates many garbage objects). - `StringBuilder`: Mutable character buffer; methods like `.append()` modify the buffer in-place without new allocations. Not synchronized (not thread-safe), but highest performance for single-threaded operations. - `StringBuffer`: Mutable character buffer; thread-safe because its methods are `synchronized`. Has locking overhead, making it slower than StringBuilder.",
        "kp": ["String is immutable to support String Constant Pool, thread safety, security, and hash caching", "StringBuilder is mutable, fast, and not thread-safe (preferred for single-threaded concatenations)", "StringBuffer is mutable, synchronized, and thread-safe with locking overhead"],
        "crit": ["Clear explanation of heap memory and String Constant Pool mechanisms", "Actionable guidance on when to choose StringBuilder over String in loops"],
        "cm": ["Using string concatenation (+) inside a 10,000-iteration loop in Java", "Thinking StringBuffer and StringBuilder are identical"],
        "fu": ["What happens in memory when you execute String s = new String('abc') vs String s = 'abc'?", "How does Java 9+ Compact Strings optimize memory footprint for Latin-1 characters?"],
        "tags": ["master-bank", "ibm", "aquaairx", "java", "strings", "immutability"]
    },

    # -------------------------------------------------------------
    # PART 6: SQL AND DATABASE QUESTIONS
    # -------------------------------------------------------------
    {
        "q": "What is the difference between primary key, foreign key, and unique constraint in SQL?",
        "cat": "SQL & Analytics",
        "sub": "Relational Constraints",
        "d": "Beginner",
        "type": "technical",
        "roles": ["Data Analyst", "Software Development Engineer", "Backend Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Relational integrity constraints enforce data correctness and relational mapping across tables: 1) Primary Key (PK): Uniquely identifies each row in a database table. A table can have ONLY ONE primary key. It automatically enforces uniqueness and CANNOT contain NULL values (`NOT NULL + UNIQUE`). Creates a clustered index by default in engines like SQL Server and MySQL InnoDB. 2) Foreign Key (FK): A column or set of columns in one table that references the Primary Key of another table, enforcing referential integrity. Ensures child records cannot reference non-existent parent rows. Prevents orphan records during updates or deletions via cascading actions (`ON DELETE CASCADE`, `ON DELETE SET NULL`). Can accept NULL values (indicating optional relationship). 3) Unique Constraint: Guarantees all values in a column are distinct across the table. Unlike a primary key, a table can have MULTIPLE unique constraints, and most SQL engines permit a single NULL value (or multiple in Postgres depending on standard). Creates a non-clustered index by default.",
        "kp": ["Primary Key: 1 per table, NOT NULL + UNIQUE, clustered index default", "Foreign Key: references parent PK, enforces referential integrity, supports CASCADE actions", "Unique Constraint: multiple per table, enforces uniqueness, allows NULL"],
        "crit": ["Accurate comparison across uniqueness, NULL handling, and indexing", "Understanding relational link established by Foreign Keys"],
        "cm": ["Thinking a table can have multiple primary keys (it can have a composite primary key with multiple columns, but only one primary key)", "Thinking foreign keys cannot be NULL"],
        "fu": ["What happens when you delete a parent row configured with ON DELETE CASCADE?", "What is a surrogate key versus a natural key?"],
        "tags": ["master-bank", "ibm", "sws-ai", "sql", "keys", "rdbms", "top-30"]
    },
    {
        "q": "Write a query to find the second-highest salary from an Employee table.",
        "cat": "SQL & Analytics",
        "sub": "Analytical Queries",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["Data Analyst", "Software Development Engineer", "Backend Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "This is one of the most classic SQL interview questions. Three standard, interview-approved solutions: 1) Subquery Approach (Universal SQL): Finds the maximum salary strictly less than the overall maximum salary. Safe and returns NULL if fewer than two distinct salaries exist:\n```sql\nSELECT MAX(salary) AS second_highest_salary\nFROM Employee\nWHERE salary < (\n    SELECT MAX(salary) FROM Employee\n);\n```\n2) Window Function DENSE_RANK() (Modern enterprise SQL): Handles duplicate salaries accurately:\n```sql\nWITH RankedSalaries AS (\n    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rnk\n    FROM Employee\n)\nSELECT MAX(salary) AS second_highest_salary\nFROM RankedSalaries\nWHERE rnk = 2;\n```\n3) LIMIT & OFFSET (MySQL/PostgreSQL): Simple, but requires DISTINCT to avoid returning duplicate maximums:\n```sql\nSELECT DISTINCT salary\nFROM Employee\nORDER BY salary DESC\nLIMIT 1 OFFSET 1;\n```",
        "kp": ["Subquery using MAX() < (SELECT MAX()) is robust across all SQL dialects", "DENSE_RANK() correctly handles ties/duplicates without skipping ranks", "LIMIT 1 OFFSET 1 must use DISTINCT to avoid returning duplicate top salaries"],
        "crit": ["Correct handling of duplicate salaries and edge case where < 2 distinct salaries exist", "Clear explanation of DENSE_RANK() vs RANK()"],
        "cm": ["Using ORDER BY salary DESC LIMIT 1 OFFSET 1 without DISTINCT (fails if multiple employees earn the top salary)", "Using RANK() which skips numbers on ties instead of DENSE_RANK()"],
        "fu": ["How would you generalize this query to find the N-th highest salary?", "What is the performance implication of running subqueries versus window functions on a table with 10M rows?"],
        "tags": ["master-bank", "ibm", "sws-ai", "sql", "salary", "subqueries", "window-functions", "top-30"]
    },
    {
        "q": "Explain SQL joins (INNER, LEFT, RIGHT, FULL OUTER, CROSS, SELF) with use-case examples.",
        "cat": "SQL & Analytics",
        "sub": "Relational Joins",
        "d": "Beginner",
        "type": "technical",
        "roles": ["Data Analyst", "Software Development Engineer", "Backend Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "A SQL JOIN combines rows from two or more tables based on a related column between them: 1) INNER JOIN: Returns only rows where there is a match in BOTH tables. Rows with no counterpart in either table are discarded. Example: Customers who have placed at least one Order. 2) LEFT JOIN (LEFT OUTER JOIN): Returns ALL rows from the left table, and the matched rows from the right table. If no match exists, NULLs appear for right-table columns. Example: All registered users and their orders (users who haven't ordered show NULL). 3) RIGHT JOIN (RIGHT OUTER JOIN): Returns ALL rows from the right table, and matched rows from the left table. 4) FULL OUTER JOIN: Returns all rows when there is a match in either left or right table. Where no match exists, NULLs fill the missing side. Example: Full reconciliation between expected payments and actual bank receipts. 5) CROSS JOIN: Cartesian product of both tables; joins every row of Table A with every row of Table B (produces count(A) * count(B) rows). Example: Generating all size and color product variants. 6) SELF JOIN: A regular join where a table is joined with itself using aliases. Example: An Employee table where each employee row has a `manager_id` referencing the same table's `employee_id`.",
        "kp": ["INNER JOIN: intersection of matching records from both tables", "LEFT JOIN: all left records preserved; missing right values filled with NULL", "FULL OUTER JOIN: union of matching and non-matching records from both tables", "SELF JOIN: table joined to itself using table aliases (hierarchical employee-manager mapping)"],
        "crit": ["Clear, accurate distinction of how unmatched rows and NULL values are handled", "Real-world examples mapping business requirements to join types"],
        "cm": ["Thinking LEFT JOIN and INNER JOIN yield identical results when foreign keys can be NULL", "Forgetting to alias the table during a SELF JOIN"],
        "fu": ["How do you find records that exist in Table A but NOT in Table B using a LEFT JOIN?", "What is the difference between ON and WHERE clause filtering in a LEFT JOIN?"],
        "tags": ["master-bank", "ibm", "sws-ai", "payoda", "sql", "joins", "rdbms", "top-30"]
    },
    {
        "q": "What is database indexing, why is it used, and what are its disadvantages?",
        "cat": "SQL & Analytics",
        "sub": "Performance & Storage",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Data Analyst"],
        "stages": ["Technical", "Final"],
        "ans": "1) What is an Index: A data structure (most commonly a B-Tree or B+ Tree, or Hash index) created on one or more table columns that allows the database engine to find specific rows in O(log N) time without scanning every row in the entire table (Full Table Scan O(N)). Analogy: Like an index at the back of a textbook. 2) Advantages: Dramatically accelerates `SELECT`, `WHERE`, `JOIN`, and `ORDER BY` query execution times from seconds to single-digit milliseconds on large datasets. Enforces uniqueness when created as a unique index. 3) Disadvantages & Trade-offs: - Write Performance Penalty: Every `INSERT`, `UPDATE`, and `DELETE` operation must update both the base table data AND all associated index trees, adding latency to write-heavy systems. - Storage Overhead: Indexes consume substantial disk space and RAM memory (can equal or exceed table size if over-indexed). - Maintenance Overhead: Indexes require periodic defragmentation and statistics updates to maintain query optimizer efficiency. Best practice: Index columns with high selectivity (cardinality) frequently used in JOIN conditions and WHERE filters; avoid indexing low-cardinality boolean columns.",
        "kp": ["Index uses B+ Tree data structure for O(log N) search, range scans, and sorting", "Dramatically reduces query latency on large tables", "Disadvantage: slows down write operations (INSERT/UPDATE/DELETE) due to tree maintenance", "Disadvantage: consumes additional disk space and memory buffer cache"],
        "crit": ["Balanced explanation covering both query acceleration and write-path overhead", "Understanding B-Tree mechanics and column selectivity"],
        "cm": ["Recommending indexing every single column in a database table", "Thinking indexes speed up INSERT operations"],
        "fu": ["What is the difference between a clustered index and a non-clustered index?", "Why are B+ Trees preferred over binary search trees for database indexes?"],
        "tags": ["master-bank", "ibm", "sws-ai", "sql", "indexing", "performance", "top-30"]
    },

    # -------------------------------------------------------------
    # PART 7: GIT, GITHUB, AND CI/CD QUESTIONS
    # -------------------------------------------------------------
    {
        "q": "What is the difference between Git and GitHub, and why is version control essential?",
        "cat": "Git & CI/CD",
        "sub": "Version Control Fundamentals",
        "d": "Beginner",
        "type": "technical",
        "roles": ["Software Development Engineer", "Full-Stack Developer", "AI Engineer"],
        "stages": ["Technical Screening", "HR"],
        "ans": "1) Git: A distributed version control system (CLI tool / software) installed locally on an engineer's computer. It tracks historical changes in source files, maintains commit snapshots, manages local branching and merging, and functions completely offline without an internet connection. 2) GitHub: A cloud-based hosting platform and collaboration service for Git repositories. It provides a visual web interface and team collaboration features beyond local Git: Pull Requests, code review discussions, issue tracking, project boards, role-based access control, and automated CI/CD pipelines via GitHub Actions. 3) Why Version Control is Essential: - Historical Audit Trail: Every change is tracked with author name, timestamp, and commit rationale; facilitates reverting regressions cleanly. - Branching & Parallel Collaboration: Multiple developers work on separate features concurrently without overwriting each other's code. - Release Management & Backup: Safely tag releases, roll back production bugs, and maintain cloud backups of intellectual property.",
        "kp": ["Git is local software for tracking changes; GitHub is a cloud hosting and collaboration service", "Git works offline; GitHub requires internet connectivity", "Version control enables concurrent branching, accountability, and seamless rollbacks"],
        "crit": ["Clear, accurate distinction between tool and hosting platform", "Articulates real software collaboration benefits (PRs, code reviews, audit trails)"],
        "cm": ["Confusing Git with GitHub as if they are the exact same entity", "Thinking Git requires an internet connection to create commits or branches"],
        "fu": ["What is the difference between 'git pull' and 'git fetch'?", "How do you resolve a merge conflict when two developers modify the same file?"],
        "tags": ["master-bank", "ibm", "aquaairx", "git", "github", "version-control", "top-30"]
    },
    {
        "q": "What is CI/CD, and how do you configure an automated pipeline using GitHub Actions?",
        "cat": "Git & CI/CD",
        "sub": "Continuous Integration & Deployment",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "DevOps Engineer"],
        "stages": ["Technical"],
        "ans": "1) CI (Continuous Integration): The engineering practice of automatically building, linting, and running automated test suites whenever code is committed or merged into a shared repository. Catches bugs, syntax breaks, and regression failures immediately before code enters main branches. 2) CD (Continuous Delivery / Deployment): The practice of automatically packaging and deploying validated software to staging or production environments without manual server intervention. 3) GitHub Actions Workflow: Configured by placing YAML files in `.github/workflows/` directory. Structure: - Events (`on: [push, pull_request]`): Defines triggers. - Runners (`runs-on: ubuntu-latest`): Cloud virtual machines running the workflow. - Jobs & Steps: Defines sequential actions (checking out repo, setting up Python/Node, caching dependencies, running `pytest` or `npm test`, and building Docker images). Example YAML:\n```yaml\nname: Test & Lint\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with: { python-version: '3.12' }\n      - run: pip install -r requirements.txt\n      - run: pytest tests/\n```",
        "kp": ["CI: automated build, lint, and test validation on commit or PR", "CD: automated deployment to staging/production environments", "GitHub Actions uses YAML workflows placed in .github/workflows/", "Protects production reliability by blocking buggy merges"],
        "crit": ["Clear explanation of CI/CD value in production software delivery", "Knowledge of workflow YAML structure: triggers, runners, and steps"],
        "cm": ["Saying CI/CD is just a fancy name for running git push", "Stating that secrets/passwords should be hardcoded in YAML files instead of GitHub Secrets"],
        "fu": ["How do you store and access private API keys securely in a GitHub Actions pipeline?", "What is the difference between Continuous Delivery and Continuous Deployment?"],
        "tags": ["master-bank", "ibm", "devops", "github-actions", "cicd", "automation"]
    },

    # -------------------------------------------------------------
    # PART 8: WEB DEVELOPMENT QUESTIONS
    # -------------------------------------------------------------
    {
        "q": "What is the difference between props and state in React, and how does state management work?",
        "cat": "Web Development",
        "sub": "React Architecture",
        "d": "Beginner",
        "type": "technical",
        "roles": ["Full-Stack Developer", "Frontend Developer", "Software Development Engineer"],
        "stages": ["Technical"],
        "ans": "In React's component-based architecture, both props and state are plain JavaScript objects that hold data controlling UI rendering, but differ in ownership and mutability: 1) Props (Properties): - Passed into a component from its parent (external data source). - Read-only (immutable) within the receiving child component; children must never modify incoming props directly. - Enables parent-to-child data flow and component configurability/reusability. 2) State: - Internal data managed and owned privately within the component itself. - Mutable via dedicated setter functions (`useState` hook or `this.setState`). - When state changes via its setter, React triggers an asynchronous re-render of the component and its children to reflect the updated UI. 3) State Management Levels: - Local Component State (`useState`, `useReducer`): Form inputs, toggles, modal visibility. - Shared / Global State (React Context API, Zustand, Redux): User authentication session, theme toggles, shopping cart items accessed across multiple routes.",
        "kp": ["Props: external, passed from parent, read-only/immutable inside child", "State: internal, owned by component, mutable via setter functions", "State mutations trigger component re-renders to synchronize DOM with data", "Global state libraries (Zustand, Redux, Context) avoid deep prop drilling"],
        "crit": ["Accurate, distinct comparison of props vs state", "Understanding unidirectional data flow in React"],
        "cm": ["Attempting to directly mutate props inside a child component (e.g. props.count = 5)", "Directly mutating state variables without using setter functions"],
        "fu": ["What is 'prop drilling' and how do you resolve it using Context or Zustand?", "Why should state updates be treated as asynchronous in React?"],
        "tags": ["master-bank", "wheelson", "sws-ai", "react", "frontend", "props-state", "top-30"]
    },
    {
        "q": "What is FastAPI, why is it chosen for modern backends, and how do async/await work?",
        "cat": "Web Development",
        "sub": "Backend & API Architecture",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["Backend Developer", "Full-Stack Developer", "AI Engineer"],
        "stages": ["Technical"],
        "ans": "1) What is FastAPI: A modern, high-performance web framework for building RESTful APIs with Python 3.8+ based on standard Python type hints, Starlette (for web routing and async capabilities), and Pydantic (for data validation and schema serialization). 2) Why Choose FastAPI: - Exceptional Speed: On par with NodeJS and Go due to ASGI asynchronous event loop architecture. - Automatic Interactive Documentation: Generates interactive Swagger UI (`/docs`) and ReDoc (`/redoc`) automatically from type hints. - Robust Type Safety & Validation: Pydantic automatically validates incoming JSON request payloads, query params, and paths, returning structured 422 Unprocessable Entity errors on invalid inputs. - Developer Velocity: Reduces boilerplate code by 40%. 3) Synchronous vs Asynchronous (`async/await`): - Synchronous (blocking): While waiting for slow I/O operations (database queries, network requests, reading disk files), the operating system thread blocks and remains idle, unable to process other incoming users. - Asynchronous (`async def` with `await`): When an endpoint encounters an `await db.execute()` call, it yields control back to the event loop. The single worker thread can handle hundreds of other concurrent incoming user requests while waiting for the I/O operation to complete, delivering massive concurrency.",
        "kp": ["FastAPI built on ASGI (Starlette) and Pydantic for high-performance async APIs", "Automatic OpenAPI/Swagger interactive documentation generation", "Pydantic type hints enforce rigorous request validation and serialization", "async/await non-blocking concurrency handles high concurrent I/O with minimal threads"],
        "crit": ["Clear articulation of ASGI event loop mechanics and non-blocking I/O", "Knowledge of Pydantic validation and auto-generated Swagger docs"],
        "cm": ["Using time.sleep() inside an async def endpoint (blocks the entire event loop thread)", "Thinking FastAPI is purely for machine learning rather than general backend web development"],
        "fu": ["What is the difference between ASGI and WSGI (Flask/Django)?", "How does FastAPI handle dependency injection using Depends()?"],
        "tags": ["master-bank", "wheelson", "sws-ai", "fastapi", "python", "backend", "async-await"]
    },
    {
        "q": "What is JWT, and how does JWT-based authentication work between frontend and backend?",
        "cat": "Web Development",
        "sub": "API Security & Authentication",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Full-Stack Developer"],
        "stages": ["Technical", "Final"],
        "ans": "JSON Web Token (JWT) is an open standard (RFC 7519) for securely transmitting compact, self-contained information between parties as a verifiable JSON object. 1) JWT Structure: Three parts separated by dots (`header.payload.signature`): - Header: Specifies token type (`JWT`) and signing algorithm (e.g., `HS256`, `RS256`). - Payload: Contains claims (user ID, username, expiration timestamp `exp`, roles). Not encrypted by default; only Base64Url encoded. - Signature: Hash of (Header + Payload + Secret Key) generated by the server. Guarantees the payload was not tampered with in transit. 2) Authentication Flow: - Client submits credentials (`POST /api/auth/login` with email and password). - Server validates password against hashed password in database. - Server generates a signed JWT and returns it to client. - Client stores token (preferably in secure `HttpOnly` cookie or memory) and attaches it to subsequent requests in the `Authorization: Bearer <token>` HTTP header. - Server verifies token signature using its secret key without querying the user database on every request, making it completely stateless and scalable.",
        "kp": ["Stateless authentication: server verifies signature without database session lookups", "Token composed of Header, Claims Payload, and Cryptographic Signature", "Client attaches token via Authorization: Bearer <token> header", "Security: sensitive secrets/passwords must never be stored inside unencrypted payload"],
        "crit": ["Complete explanation of token lifecycle and cryptographic verification", "Security considerations (HttpOnly cookies vs LocalStorage, token expiration)"],
        "cm": ["Believing JWT encrypts data (it only signs data; anyone can decode base64 payload)", "Setting infinite expiration times on tokens"],
        "fu": ["What is the difference between an Access Token and a Refresh Token?", "How do you revoke or invalidate a stateless JWT before its expiration timestamp?"],
        "tags": ["master-bank", "wheelson", "sws-ai", "security", "jwt", "authentication"]
    },

    # -------------------------------------------------------------
    # PART 9: ARTIFICIAL INTELLIGENCE, ML, DEEP LEARNING & RAG
    # -------------------------------------------------------------
    {
        "q": "What is the difference between precision, recall, and F1-score, and how do you handle class imbalance?",
        "cat": "ML, AI & GenAI",
        "sub": "Model Evaluation & Imbalanced Data",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["Machine Learning Engineer", "AI Engineer", "Data Scientist"],
        "stages": ["Technical"],
        "ans": "1) Metrics: - Precision = TP / (TP + FP). Out of all instances the model predicted as positive, how many were actually positive? Crucial when False Positives are costly (e.g., email spam filter: an important email must not be sent to spam). - Recall (Sensitivity) = TP / (TP + FN). Out of all actual positive instances, how many did the model correctly catch? Crucial when False Negatives are catastrophic (e.g., cancer detection, fraud detection: missing a disease is life-threatening). - F1-Score = 2 * (Precision * Recall) / (Precision + Recall). The harmonic mean balancing precision and recall. Accuracy is deceptive on imbalanced datasets (e.g., in a dataset with 99% negative cases, a naive model predicting 100% negative achieves 99% accuracy but 0% recall). 2) Handling Class Imbalance: - Resampling: SMOTE (Synthetic Minority Over-sampling Technique) to generate synthetic minority samples, or Random Under-sampling. - Class Weights: Adjust loss function penalties (e.g., `class_weight='balanced'` in scikit-learn or `scale_pos_weight` in XGBoost) to penalize minority misclassifications more heavily. - Threshold Tuning: Adjust classification decision threshold from default 0.5 to optimize Precision-Recall curves. - Metric Choice: Optimize for ROC-AUC and PR-AUC instead of standard accuracy.",
        "kp": ["Precision: penalizes false positives; Recall: penalizes false negatives", "F1-Score: harmonic mean useful when dataset is imbalanced", "Accuracy is deceptive when class distributions are skewed (e.g. 99:1)", "Mitigate imbalance via SMOTE, class-weighted loss functions, and PR-AUC optimization"],
        "crit": ["Clear mathematical formulation and real-world domain trade-offs", "Concrete technical techniques to mitigate severe class imbalance"],
        "cm": ["Relying solely on Accuracy when evaluating fraud detection or medical diagnosis models", "Confusing Precision with Recall"],
        "fu": ["When would you prefer PR-AUC over ROC-AUC on highly skewed datasets?", "How does SMOTE synthesize new data points without simple duplication?"],
        "tags": ["master-bank", "payoda", "sws-ai", "ibm", "machine-learning", "metrics", "imbalance", "top-30"]
    },
    {
        "q": "What is the difference between prompt engineering, fine-tuning, and Retrieval-Augmented Generation (RAG)?",
        "cat": "ML, AI & GenAI",
        "sub": "LLM Customization Strategies",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["AI Engineer", "Generative AI Engineer", "Software Development Engineer"],
        "stages": ["Technical", "Final"],
        "ans": "These represent the three primary levels of customizing Large Language Models (LLMs): 1) Prompt Engineering: - What: Crafting, structuring, and optimizing the natural language instructions and context passed to a frozen foundation model (zero-shot, few-shot examples, Chain-of-Thought). - When: Best for quick prototyping, formatting outputs (JSON), and general tasks requiring no custom knowledge. - Pros: Zero training cost, immediate iteration. - Cons: Constrained by context window limits; cannot add vast private company knowledge. 2) RAG (Retrieval-Augmented Generation): - What: Dynamically retrieving relevant factual context chunks from an external knowledge base (vector database, SQL database) based on the user's query and injecting them into the LLM's prompt before generation. - When: Ideal for private, dynamic company data, document QA, and reducing hallucinations with source citations. - Pros: Never modifies model weights; data can be updated in real time; transparent source attribution. - Cons: Requires indexing pipeline (chunking, embedding, vector search). 3) Fine-Tuning: - What: Training model weights further on a specialized dataset using techniques like LoRA/PEFT or full-parameter tuning. - When: Best for teaching the model a specific style, specialized medical/legal vocabulary, or domain-specific tone/syntax. - Pros: Bakes behavior into the weights; reduces prompt token costs. - Cons: High compute cost, potential catastrophic forgetting, and requires retraining whenever factual knowledge updates.",
        "kp": ["Prompt Engineering: optimize instructions for a frozen model (zero/few-shot)", "RAG: inject dynamically retrieved external factual context into prompt at query time", "Fine-Tuning: retrain model weights (LoRA/PEFT) to adapt style, syntax, and specialized tone", "RAG is best for dynamic factual knowledge; Fine-Tuning is best for behavioral specialization"],
        "crit": ["Clear, accurate distinction of trade-offs: cost, latency, update frequency, and hallucination reduction", "Understanding when to combine RAG with Fine-Tuning"],
        "cm": ["Assuming fine-tuning is required just to answer questions about a PDF document (RAG is appropriate)", "Assuming RAG updates the neural network's underlying weights"],
        "fu": ["How do you evaluate retrieval precision versus generator hallucination in a RAG pipeline?", "What is LoRA (Low-Rank Adaptation) and how does it reduce fine-tuning memory?"],
        "tags": ["master-bank", "sws-ai", "ibm", "payoda", "genai", "rag", "fine-tuning", "llm", "top-30"]
    },
    {
        "q": "What is an AI Agent, and what is the difference between an AI agent and a conventional chatbot?",
        "cat": "ML, AI & GenAI",
        "sub": "Agentic AI & Orchestration",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["AI Engineer", "Generative AI Engineer", "Software Development Engineer"],
        "stages": ["Technical", "Final"],
        "ans": "1) Conventional Chatbot: A reactive system that receives a user prompt and generates a single text response based on learned weights or simple retrieval. It has no autonomy, cannot call external software tools, cannot execute multi-step planning, and cannot take actions in external software systems. 2) AI Agent: An autonomous software entity that uses an LLM as its core reasoning engine to accomplish high-level user goals through multi-step planning, memory, and tool execution. 3) Core Components of an AI Agent: - Planning / Reasoning: Decomposes complex goals into sequential sub-tasks (e.g., ReAct framework: Reason -> Act -> Observe loop). - Memory: Short-term memory (in-context conversation trajectory) and Long-term memory (vector database of past interactions and facts). - Tools / Function Calling: Interfaces to call external APIs, execute Python code, query SQL databases, or browse the web. - Environment & Execution Loop: Acts on an environment, receives feedback from tool outputs, self-corrects upon errors, and loops until the goal is achieved. Illustrative example: Asking a chatbot 'Find available flights and book the cheapest one' yields text advice. An AI agent queries airline APIs, compares prices, invokes a payment gateway tool, and returns a verified booking confirmation.",
        "kp": ["Chatbot is a reactive text generator; Agent is an autonomous goal-driven system", "Agent architecture: LLM reasoning core + Planning + Memory + Tools (API/code execution)", "ReAct cycle: Reason -> Act (call tool) -> Observe (parse output) -> Iterate until goal satisfied"],
        "crit": ["Clear differentiation between passive conversational interfaces and active agentic systems", "Understanding function calling, memory layers, and multi-step plan orchestration"],
        "cm": ["Assuming any LLM chatbot is automatically an AI agent", "Ignoring error handling and infinite loops in agent execution cycles"],
        "fu": ["What is agent orchestration, and how do multi-agent frameworks (LangGraph, CrewAI, AutoGen) work?", "How do you prevent an AI agent from executing dangerous or malicious external tool actions?"],
        "tags": ["master-bank", "sws-ai", "ai-agents", "agentic-ai", "llm", "top-30"]
    },

    # -------------------------------------------------------------
    # PART 10: NETWORKING, CYBERSECURITY, AND IOT QUESTIONS
    # -------------------------------------------------------------
    {
        "q": "Explain the seven layers of the OSI model and the difference between TCP and UDP.",
        "cat": "Networking & IoT",
        "sub": "Computer Networking",
        "d": "Beginner",
        "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "1) OSI 7-Layer Reference Model (Top to Bottom): - Layer 7 (Application): End-user protocols (HTTP, HTTPS, FTP, DNS, SMTP). - Layer 6 (Presentation): Data translation, encryption, formatting, compression (SSL/TLS, JSON, JPEG). - Layer 5 (Session): Manages and terminates communication sessions between applications (RPC, NetBIOS). - Layer 4 (Transport): End-to-end communication, flow control, reliability, port addressing (TCP, UDP). - Layer 3 (Network): Logical addressing (IP addresses) and routing packets across subnets (IP, ICMP, Routers). - Layer 2 (Data Link): Physical addressing (MAC addresses), frame delivery, error checking on local link (Ethernet, Switches). - Layer 1 (Physical): Physical transmission of raw binary bits over cables, fiber optics, or radio frequencies. 2) TCP vs. UDP: - TCP (Transmission Control Protocol): Connection-oriented (3-way handshake SYN -> SYN-ACK -> ACK). Reliable: guarantees in-order packet delivery, error checking, and retransmission of lost packets. Flow and congestion control. Higher overhead; used for web browsing (HTTP/HTTPS), file transfer (FTP), email. - UDP (User Datagram Protocol): Connectionless; fires packets without prior handshake. Unreliable: no guaranteed delivery, no order preservation, no retransmission. Lightweight, low latency, minimal overhead; used for live video streaming (VoIP, YouTube live), online multiplayer gaming, and DNS queries.",
        "kp": ["OSI 7 Layers: Application, Presentation, Session, Transport, Network, Data Link, Physical", "TCP: connection-oriented, reliable, in-order, 3-way handshake, retransmission (HTTP, SSH)", "UDP: connectionless, lightweight, low-latency, packet loss tolerated (DNS, VoIP, gaming)"],
        "crit": ["Systematic memory of all 7 layers with their primary functions", "Clear, accurate distinction between TCP reliability vs UDP speed"],
        "cm": ["Confusing IP addresses (Layer 3) with MAC addresses (Layer 2)", "Thinking UDP is always 'worse' than TCP (it is intentionally optimized for low latency)"],
        "fu": ["What happens step-by-step during a TCP 3-way handshake?", "At which OSI layers do firewalls and load balancers operate?"],
        "tags": ["master-bank", "ibm", "aquaairx", "networking", "osi-model", "tcp-udp", "top-30"]
    },
    {
        "q": "What is the Internet of Things (IoT), how do IoT devices communicate, and what are their security challenges?",
        "cat": "Networking & IoT",
        "sub": "IoT Architecture & Security",
        "d": "Intermediate",
        "type": "technical",
        "roles": ["Software Development Engineer", "Embedded Engineer", "Full-Stack Developer"],
        "stages": ["Technical"],
        "ans": "1) What is IoT: A network of physical devices ('things') equipped with sensors, actuators, processing ability, and network connectivity that collect and exchange telemetry data with cloud platforms or other devices without requiring direct human intervention. Examples: Smart environmental monitors, connected vehicles, smart home automation, industrial predictive maintenance sensors. 2) Communication Protocols: - MQTT (Message Queuing Telemetry Transport): Lightweight publish-subscribe messaging protocol designed for constrained devices with limited bandwidth and battery life. - CoAP (Constrained Application Protocol): REST-like protocol over UDP for low-power microcontrollers. - Wireless Standards: Wi-Fi, BLE (Bluetooth Low Energy), Zigbee, LoRaWAN (Long Range Wide Area Network for rural/city sensor arrays). 3) Security Challenges: - Constrained Compute & Memory: Microcontrollers often lack CPU power to run heavy asymmetric cryptographic ciphers or frequent TLS handshakes. - Default Credentials: Many commercial IoT devices ship with hardcoded default passwords (e.g., Mirai botnet exploits). - Insecure Firmware Updates: Lack of over-the-air (OTA) cryptographic firmware signature verification allows malicious firmware flashing. - Physical Tampering: Devices installed in open environments can be physically tapped to extract cryptographic keys.",
        "kp": ["IoT connects physical sensors and actuators to cloud telemetry systems", "Lightweight protocols: MQTT (pub-sub) and CoAP over UDP for low-power constraints", "Security risks: weak compute for encryption, hardcoded default credentials, lack of signed OTA updates"],
        "crit": ["Understanding constrained hardware limitations versus enterprise server capabilities", "Practical knowledge of MQTT pub-sub architecture and real IoT attack surfaces"],
        "cm": ["Assuming IoT devices use standard heavy HTTP/REST requests for frequent sensor heartbeats", "Ignoring physical security and power consumption constraints"],
        "fu": ["What is MQTT Quality of Service (QoS 0, 1, 2) and how does it guarantee message delivery?", "How does an IoT gateway act as an intermediary between edge devices and the cloud?"],
        "tags": ["master-bank", "hexaware", "wheelson", "aquaairx", "iot", "protocols", "mqtt"]
    },

    # -------------------------------------------------------------
    # PART 12: QUESTIONS TO ASK THE INTERVIEWER
    # -------------------------------------------------------------
    {
        "q": "What thoughtful questions should a candidate ask the interviewer at the end of an interview?",
        "cat": "Company & Workplace",
        "sub": "Questions for Interviewer",
        "d": "Beginner",
        "type": "hr",
        "roles": ["Software Development Engineer", "AI Engineer", "Data Analyst", "Full-Stack Developer"],
        "stages": ["Final", "HR", "Technical"],
        "ans": "Asking insightful questions demonstrates genuine curiosity, intellectual engagement, and career seriousness. Always prepare 2-3 tailored questions based on the interviewer's role: 1) For a Technical Lead / Engineering Manager: - 'What does the tech stack and engineering deployment pipeline look like on the specific team I would join?' - 'What are the technical benchmarks or skills you expect a fresher to develop in their first 90 days to become fully productive?' - 'How does the team handle code reviews, testing standards, and balancing technical debt against new feature velocity?' 2) For an HR / Campus Recruiter: - 'How is the onboarding and mentorship structured for new graduates entering the organization?' - 'What opportunities exist for engineers to rotate across domains such as AI, backend, or cloud infrastructure?' - 'What are the subsequent steps in the interview evaluation timeline?' What to AVOID asking: Never ask questions answered in the first five minutes of the company presentation (e.g., 'What does your company do?'), and avoid asking about immediate vacation policies or bonuses during an initial technical round.",
        "kp": ["Demonstrate genuine interest in engineering standards, mentorship, and team workflows", "Tailor questions appropriately to technical leads vs HR recruiters", "Focus on first 90-day productivity, learning curve, and code review culture", "Avoid asking basic questions already covered on the company's public website"],
        "crit": ["Professional, insightful inquiry showcasing ambition and cultural readiness", "Clear distinction between technical vs HR questions"],
        "cm": ["Saying 'No, I have no questions' (signals disinterest or passivity)", "Asking 'How did I do?' or asking for immediate hiring decisions on the spot"],
        "fu": ["How do you take notes during an interview to formulate relevant follow-up questions?", "Why is asking about the team's first 90-day expectations particularly impactful for freshers?"],
        "tags": ["master-bank", "ibm", "hexaware", "aquaairx", "payoda", "sws-ai", "wheelson", "hr", "closing-questions", "top-30"]
    }
]


def seed_master_bank() -> tuple[int, int]:
    """Inserts or updates the master bank questions in the database."""
    created = 0
    updated = 0

    with SessionLocal() as db:
        # Load all existing questions into fingerprint index
        existing_rows = db.scalars(select(Question)).all()
        hash_to_question = {row.question_hash: row for row in existing_rows}
        id_to_question = {row.id: row for row in existing_rows}

        for item in MASTER_BANK_DATA:
            q_text = item["q"]
            h = question_fingerprint(q_text)

            # Check if this question is part of the top 30
            is_top_30 = any(kw in q_text.lower() for kw in TOP_30_KEYWORDS)
            tags = list(item.get("tags", []))
            if is_top_30 and "top-30" not in tags:
                tags.append("top-30")

            if h in hash_to_question:
                # Update existing question with master bank metadata and tags
                row = hash_to_question[h]
                merged_tags = list(dict.fromkeys(list(row.tags or []) + tags))
                row.tags = merged_tags
                updated += 1
                log.info(f"Updated tags on existing question: {row.id} - {row.question[:40]}")
            else:
                # Determine clean unique ID
                cat_slug = item["cat"].lower().replace("&", "").replace(",", "").replace(" ", "-")[:4]
                sub_count = sum(1 for qid in id_to_question if qid.startswith(f"mst-{cat_slug}"))
                new_id = f"mst-{cat_slug}-{sub_count + 1:03d}"

                # Ensure ID uniqueness
                while new_id in id_to_question:
                    sub_count += 1
                    new_id = f"mst-{cat_slug}-{sub_count + 1:03d}"

                new_row = Question(
                    id=new_id,
                    question=q_text,
                    question_hash=h,
                    category=item["cat"],
                    subcategory=item["sub"],
                    difficulty=item["d"],
                    question_type=item["type"],
                    target_roles=item["roles"],
                    interview_stage=item["stages"],
                    reference_answer=item["ans"],
                    key_points=item["kp"],
                    evaluation_criteria=item["crit"],
                    common_mistakes=item["cm"],
                    follow_up_questions=item["fu"],
                    tags=tags,
                    is_active=True,
                )
                db.add(new_row)
                id_to_question[new_id] = new_row
                hash_to_question[h] = new_row
                created += 1
                log.info(f"Created new master question: {new_id} - {q_text[:40]}")

        db.commit()

    return created, updated


if __name__ == "__main__":
    c, u = seed_master_bank()
    print(f"Master Question Bank Seed Finished: Created {c} new questions, Updated {u} existing questions.")
