"""Generator for Category C: Resume, Projects, and Experience (60 questions).
20 questions in 01.json, 20 in 02.json, 20 in 03.json.
Must include 'illustrative' marker in every reference answer.
"""
import json
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parents[2] / "data" / "src" / "C_projects"

PART1 = [
    {
        "q": "Walk me through the best technical project on your resume from problem to deployment.",
        "sub": "Project Walkthrough",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: full lifecycle ownership, clarity, and architectural awareness. Structure your answer in four distinct phases: the core problem and why it mattered, your high-level architecture and technology stack, your specific implementation contributions, and the final deployment and verifiable results. Avoid getting lost in minor syntax details. Illustrative example (replace with your actual project details): 'For my project [Project Name], the problem was [Problem Statement]. I designed an architecture comprising [Frontend/Backend/Database/Model]. My primary contribution was [Specific Feature/Module], and we deployed it using [Docker/Cloud/Vercel], resulting in [Measurable Metric or User Outcome].'",
        "kp": ["Clear problem statement and motivation", "Architectural overview without jargon", "Precise individual contribution", "Deployment strategy and measurable outcome"],
        "cm": ["Listing technologies without explaining why they were chosen", "Using 'we' without clarifying your personal role", "Focusing on UI only while ignoring backend/architecture", "No measurable outcome or testing mentioned"],
        "fu": ["What was the most difficult architectural decision you had to make?", "How did you measure that the project actually solved the user problem?"],
        "tags": ["project-walkthrough", "architecture", "resume", "fresher"]
    },
    {
        "q": "What was the core problem your final-year capstone project aimed to solve, and who was the intended user?",
        "sub": "Problem Statement",
        "d": "Beginner",
        "ans": "Interviewer is assessing: problem-solving mindset, empathy for end-users, and product thinking. Clearly state who the target users were, the exact pain point they experienced, why existing solutions were inadequate, and how your project addressed that gap. Show that you built something for a real purpose, not just for academic marks. Illustrative example (replace with your actual project details): 'The intended users were [Target Users], who struggled with [Specific Pain Point]. Existing tools were either [Limitation 1] or [Limitation 2]. Our application addressed this by [Core Value Proposition], which allowed users to [Key Benefit].'",
        "kp": ["Specific target audience identified", "Clear pain point articulated", "Comparison with existing alternatives", "Direct link between problem and technical features"],
        "cm": ["Vague target audience like 'everyone'", "Describing features before explaining the problem", "Building a clone without explaining any unique value or purpose"],
        "fu": ["Did you validate this problem with any real users before building?", "If you commercialized this today, what would be your biggest challenge?"],
        "tags": ["problem-statement", "product-thinking", "capstone", "fresher"]
    },
    {
        "q": "Why did you choose your specific technology stack for your main project over popular alternatives?",
        "sub": "Technology Choices",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: engineering trade-off analysis and technical decision-making. Explain the criteria that guided your choice—such as development speed, library ecosystem, performance, scalability, or learning curve. Contrast your chosen stack with at least one viable alternative and justify why your choice was the most suitable for the project's constraints. Illustrative example (replace with your actual project details): 'We selected FastAPI over Django because our application was primarily API-driven with asynchronous I/O requirements for machine learning inferences. While Django provides an out-of-the-box admin panel, FastAPI gave us native async support, automatic OpenAPI documentation, and minimal overhead.'",
        "kp": ["Comparison against viable alternatives", "Objective criteria: speed, async, libraries, constraints", "Understanding of chosen stack's strengths and weaknesses", "No blind adherence to hype"],
        "cm": ["Saying 'I chose it because it is popular' or 'it was the only one I knew'", "Not acknowledging trade-offs or weaknesses of the stack", "Attacking alternative technologies unfairly"],
        "fu": ["If you had to scale this application 10x, where would this stack bottle-neck first?", "What would make you choose the alternative framework on your next project?"],
        "tags": ["tech-stack", "trade-offs", "architecture", "engineering-decisions"]
    },
    {
        "q": "What was your exact individual contribution in your team project, and how did you collaborate with teammates?",
        "sub": "Personal Contribution",
        "d": "Beginner",
        "ans": "Interviewer is assessing: honesty, accountability, and team collaboration. Explicitly delineate what modules, APIs, or database schemas you personally designed and wrote versus what your teammates handled. Mention how you managed version control, code reviews, task tracking, and interface contracts. Illustrative example (replace with your actual project details): 'Our team had four members. I took complete ownership of the authentication subsystem, the PostgreSQL database schema design, and the RESTful endpoints for order processing. We used Git feature branches, conducted peer pull request reviews, and documented API contracts in Swagger so the frontend team could develop concurrently.'",
        "kp": ["Exact boundaries of personal contribution", "Ownership of specific modules and codebases", "Collaboration tools: Git, branches, PRs, API contracts", "Support provided to unblock teammates"],
        "cm": ["Taking 100% credit for a multi-member project", "Using vague phrases like 'I contributed to everything'", "Blaming teammates for delays or weak areas"],
        "fu": ["What happened when your backend contracts changed unexpectedly for the frontend?", "Which part of your teammate's code did you review most critically?"],
        "tags": ["teamwork", "ownership", "git", "collaboration"]
    },
    {
        "q": "What was the single most difficult technical bug or challenge you encountered in your project, and how did you debug it?",
        "sub": "Technical Challenges",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: systematic debugging, resilience, and root-cause analysis. Use a structured explanation: describe the unexpected symptom, the hypotheses you formed, the diagnostic tools or logging you used to isolate the issue, the root cause discovered, and the permanent fix applied. Illustrative example (replace with your actual project details): 'While integrating our payment gateway, webhooks intermittently failed with 400 Bad Request errors. I initially suspected network latency. By inspecting raw HTTP payloads and server logs, I discovered that our request body parser was mutating JSON keys before cryptographic signature verification. Rewriting the webhook handler to inspect raw byte streams resolved the bug completely.'",
        "kp": ["Clear distinction between symptom and root cause", "Methodical hypothesis-driven debugging process", "Use of logs, debuggers, or network inspect tools", "Permanent preventive solution implemented"],
        "cm": ["Describing a superficial syntax error as a major challenge", "Saying 'I Googled it and copied from Stack Overflow' without understanding", "Unable to explain why the bug occurred"],
        "fu": ["How did you prevent similar regressions in future builds?", "Did you write an automated test to capture this edge case?"],
        "tags": ["debugging", "problem-solving", "troubleshooting", "resilience"]
    },
    {
        "q": "How did you test your application to ensure it was reliable and free of major edge-case bugs?",
        "sub": "Testing & Validation",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: software engineering maturity and automated quality assurance. Discuss the levels of testing you employed: unit tests for core business logic, integration tests for API endpoints and database operations, and manual user testing for edge cases. Mention testing frameworks, mock fixtures, and validation tools used. Illustrative example (replace with your actual project details): 'I wrote unit tests using pytest for our scoring calculation engine and integration tests using FastAPI TestClient with an in-memory SQLite database. We tested edge cases such as empty input payloads, invalid JWT tokens, and concurrent requests. This caught an off-by-one pagination bug before demo day.'",
        "kp": ["Multi-tier testing: unit, integration, edge cases", "Use of standard testing frameworks (pytest, Jest, JUnit)", "Mocking external services and database isolation", "Edge cases specifically tested"],
        "cm": ["Saying 'we tested manually in the browser by clicking around'", "Not knowing what a unit test or mock fixture is", "Claiming 100% test coverage without realistic evidence"],
        "fu": ["How did you test external third-party API dependencies without making live calls?", "What was the most subtle edge case that slipped past your initial test suite?"],
        "tags": ["testing", "qa", "pytest", "unit-tests"]
    },
    {
        "q": "Did you measure the performance of your system, and what steps did you take to optimize it?",
        "sub": "Performance Improvement",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: profiling skills, latency awareness, and optimization principles. Share your baseline measurements, identify where the bottleneck lay (e.g., N+1 database queries, unindexed lookups, synchronous blocking calls, large payload sizes), and explain the exact optimization applied and the verified improvement. Illustrative example (replace with your actual project details): 'Our dashboard endpoint initially took 1.4 seconds to load when querying 10,000 records. Profiling revealed an N+1 query pattern where user details were fetched inside a loop. By rewriting the query using SQLAlchemy joinedload and adding a composite index on (user_id, created_at), response latency dropped to 180ms.'",
        "kp": ["Baseline latency or throughput measurement", "Profiling to locate the exact bottleneck", "Database indexing, query optimization, or caching applied", "Measurable percentage or millisecond improvement"],
        "cm": ["Premature optimization without measurement", "Generic claims like 'I made the code faster' with zero numbers", "Confusing frontend rendering speed with backend response latency"],
        "fu": ["What trade-offs did your optimization introduce, such as increased memory or write overhead?", "How would you monitor performance degradations in production?"],
        "tags": ["performance", "optimization", "profiling", "database-indexing"]
    },
    {
        "q": "How did you handle security, authentication, and user data privacy in your application?",
        "sub": "Security & Privacy",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: security awareness, OWASP familiarity, and responsible data handling. Discuss how you implemented password hashing (e.g., bcrypt), stateless token authentication (JWT with expiration and signature verification), CORS policies, SQL injection prevention via ORMs, and secure storage of environment secrets. Illustrative example (replace with your actual project details): 'We secured credentials using bcrypt with salt rounds of 12 and generated short-lived JWT access tokens alongside HTTP-only refresh tokens. We strictly sanitized inputs via Pydantic schemas to prevent injection attacks, configured CORS headers to restrict browser origins, and stored API keys in .env files ignored by version control.'",
        "kp": ["Password hashing (bcrypt/argon2, never plain text)", "Token lifecycle (JWT, expiry, refresh tokens)", "Input validation to prevent SQLi and XSS", "Environment secrets management"],
        "cm": ["Storing plain text passwords or hardcoding API keys in GitHub", "Not knowing how JWT tokens are signed or verified", "Assuming HTTPS solves all application-layer security vulnerabilities"],
        "fu": ["How would you handle token invalidation if a user logs out before the JWT expires?", "What precautions did you take against Cross-Site Scripting (XSS) on the frontend?"],
        "tags": ["security", "jwt", "authentication", "owasp"]
    },
    {
        "q": "How did you deploy your application, and what was your deployment architecture?",
        "sub": "Deployment",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: DevOps familiarity, containerization, and production mindset. Detail the deployment environment (e.g., Docker container, cloud VM, Render, AWS EC2, or Vercel), how the frontend and backend communicate, reverse proxy configuration (Nginx), and database hosting. Mention CI/CD pipelines if applicable. Illustrative example (replace with your actual project details): 'We containerized the FastAPI backend using a multi-stage Dockerfile to minimize image size. The frontend was built and deployed to Vercel, while the backend and PostgreSQL database ran via Docker Compose on an AWS EC2 t3.micro instance. We configured an Nginx reverse proxy with SSL termination via Let\\'s Encrypt.'",
        "kp": ["Containerization using Docker", "Hosting platform and architecture components", "Reverse proxy and SSL setup", "Environment configuration and CI/CD basics"],
        "cm": ["Saying 'it runs on localhost:3000'", "Not knowing the difference between development server and production server", "Unable to explain how the frontend connects to backend in production"],
        "fu": ["How did you manage environment variables and secrets during deployment?", "What happens to persistent database data when the Docker container restarts?"],
        "tags": ["deployment", "docker", "devops", "cloud"]
    },
    {
        "q": "Walk me through the database schema you designed for your project. How did you normalize it?",
        "sub": "Database Design",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: data modeling, entity relationships, and normalization knowledge. Explain your core entities, primary and foreign key relationships (one-to-many, many-to-many), normalization level (3NF), and why any deliberate denormalization was introduced. Illustrative example (replace with your actual project details): 'Our database modeled Users, Projects, and Evaluations. A User has many Projects, while each Project has multiple Turn evaluations. We normalized entities to 3rd Normal Form to eliminate redundancy, using junction tables with composite keys for many-to-many tag associations. Foreign keys enforced cascading deletions to prevent orphaned records.'",
        "kp": ["Key entities and their relationships (1:1, 1:N, N:M)", "Normalization rationale (1NF, 2NF, 3NF)", "Primary keys, foreign keys, and referential integrity", "Judicious use of indexing or JSONB for unstructured fields"],
        "cm": ["Putting all data in a single massive flat table", "Not knowing what 3NF or referential integrity means", "Forgetting foreign keys and index constraints"],
        "fu": ["Why did you choose a relational SQL database over MongoDB or NoSQL?", "How did you handle database schema migrations across deployments?"],
        "tags": ["database-design", "sql", "normalization", "schema"]
    },
    {
        "q": "How did you design your REST API endpoints? What conventions and status codes did you follow?",
        "sub": "API Design",
        "d": "Beginner",
        "ans": "Interviewer is assessing: RESTful principles, HTTP protocol knowledge, and API contract clarity. Explain how you named resources hierarchically using plural nouns, mapped HTTP verbs (GET, POST, PUT, DELETE, PATCH) to CRUD operations, and returned appropriate HTTP status codes (200, 201, 204, 400, 401, 404, 422, 500) with uniform error payload structures. Illustrative example (replace with your actual project details): 'I designed our APIs following REST conventions, using plural resource nouns such as /api/v1/sessions and /api/v1/sessions/{id}/turns. We returned 201 Created on resource insertion with the created record, 204 No Content on soft delete, and 422 Unprocessable Entity for schema validation failures with detailed field-level error messages.'",
        "kp": ["Plural noun naming conventions (/users, /orders)", "Correct HTTP verb usage (GET, POST, PUT, DELETE)", "Accurate HTTP status codes (200, 201, 400, 401, 404, 422)", "Consistent JSON response and error contracts"],
        "cm": ["Using verbs in endpoint paths like /getUsers or /deleteOrder", "Returning 200 OK for errors with a message {status: 'error'}", "Ignoring pagination on endpoints returning lists"],
        "fu": ["What is the difference between PUT and PATCH in your API design?", "How did you implement pagination and filtering on list endpoints?"],
        "tags": ["api-design", "rest", "http", "backend"]
    },
    {
        "q": "What are the biggest limitations of your project in its current state?",
        "sub": "Limitations",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: critical self-awareness, technical honesty, and engineering maturity. Every real project has trade-offs and boundaries. State two or three genuine limitations—such as concurrency constraints, lack of caching, dependency on a single model provider, or simplified business rules—without diminishing your actual accomplishment. Illustrative example (replace with your actual project details): 'The primary limitation currently is scalability during traffic spikes: because we generate AI evaluations synchronously without a task queue, simultaneous users experience increased queueing latency. Additionally, our session state relies entirely on PostgreSQL queries without a Redis caching layer for rapid read retrieval.'",
        "kp": ["Honest, well-understood limitations", "Rooted in architecture rather than superficial complaints", "Shows awareness of production scale realities", "Demonstrates technical self-awareness"],
        "cm": ["Claiming 'there are no limitations; it works perfectly'", "Naming fatal flaws that suggest complete carelessness", "Being overly apologetic or defensive"],
        "fu": ["If you had one more sprint, which of these limitations would you solve first?", "How would you re-architect the system to eliminate that bottleneck?"],
        "tags": ["limitations", "self-awareness", "architecture", "trade-offs"]
    },
    {
        "q": "What major trade-offs did you make during project development, and why did you choose that path?",
        "sub": "Trade-offs",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: engineering pragmatism and decision-making under constraints. Software development requires balancing speed vs perfection, simplicity vs flexibility, and consistency vs latency. Explain a specific trade-off you faced, the two competing options, and why you settled on your decision. Illustrative example (replace with your actual project details): 'We traded off real-time WebSockets communication for HTTP polling in our first version. While WebSockets offer lower latency, standard REST endpoints simplified session reconnection, error retry handling, and load balancer setup, allowing us to ship a reliable MVP three weeks ahead of demo day.'",
        "kp": ["Identification of competing engineering priorities", "Clear rationale for the chosen path", "Awareness of what was sacrificed", "Pragmatism aligned with project deadlines"],
        "cm": ["Saying there were no trade-offs", "Choosing complex solutions just for resume buzzwords", "Failing to explain why the alternative was rejected"],
        "fu": ["At what user volume would that trade-off no longer be acceptable?", "Would you make the exact same choice in hindsight?"],
        "tags": ["trade-offs", "engineering-decisions", "architecture"]
    },
    {
        "q": "If you had two more months to work on this project, what would you add or re-architect?",
        "sub": "Future Improvements",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: vision, technical ambition, and ongoing interest in the project. Outline a prioritized roadmap covering architecture improvements, new capabilities, and operational robustness (such as monitoring, automated CI/CD, or asynchronous processing). Illustrative example (replace with your actual project details): 'First, I would introduce Celery with Redis for asynchronous background evaluation to unblock the main web workers. Second, I would implement OpenTelemetry for request tracing and latency observability. Third, I would add a fine-tuned lightweight model on self-hosted vLLM to cut Groq inference costs for standard rubrics.'",
        "kp": ["Prioritized roadmap (architecture, features, observability)", "Specific modern technologies mentioned with clear purpose", "Focus on scalability, user experience, and cost", "Shows genuine excitement about the engineering domain"],
        "cm": ["Saying 'I don't know, it's done for college'", "Listing superficial UI color changes as top priority", "Suggesting random unrelated hype technologies"],
        "fu": ["How would you prioritize between adding new features versus refactoring the backend?", "What would be the estimated complexity of adding that asynchronous queue?"],
        "tags": ["future-improvements", "roadmap", "architecture", "vision"]
    },
    {
        "q": "Tell me about a feature in your project that failed or had to be scrapped completely. What happened?",
        "sub": "Project Failure",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: adaptability, humility, and ability to pivot when data contradicts assumptions. Describe what feature you attempted, the technical or user problem that made it unviable, how you recognized the failure early, and what you replaced it with or learned from it. Illustrative example (replace with your actual project details): 'We initially attempted to run a local 7B parameter open-source LLM directly on our free-tier cloud instance for real-time interview evaluation. The instance quickly suffered out-of-memory crashes, and response latency exceeded 45 seconds. Recognizing this unviability, we pivoted to Groq\\'s hosted API, reducing latency to 800ms while maintaining zero infrastructure costs within tier limits.'",
        "kp": ["Objective description of the failed initiative", "Data-driven recognition of failure", "Decisive pivot to an effective alternative", "Mature reflection on the engineering lesson"],
        "cm": ["Claiming that nothing ever failed", "Blaming cloud providers or teammates for the failure", "Dwelling on frustration rather than the solution"],
        "fu": ["What early warning signs did you overlook before building that feature?", "How has this experience changed how you evaluate third-party tools today?"],
        "tags": ["failure", "pivot", "learning", "adaptability"]
    },
    {
        "q": "How did you explain your technical project to non-technical stakeholders, professors, or business judges?",
        "sub": "Communication",
        "d": "Beginner",
        "ans": "Interviewer is assessing: verbal clarity, audience adaptation, and ability to translate tech to business value. Explain how you avoided acronyms and low-level code details, grounded the explanation in the real-world problem and user workflow, used intuitive analogies, and highlighted business outcomes or time saved. Illustrative example (replace with your actual project details): 'When presenting to department evaluators who were unfamiliar with vector embeddings, I used the analogy of a smart library indexing system that finds books based on meaning rather than exact word matching. I focused on the practical problem—students failing HR interviews due to lack of feedback—and demonstrated the step-by-step user journey before showing the architecture diagram.'",
        "kp": ["Translating technical jargon into relatable analogies", "Focusing on user value and real-world outcomes", "Interactive demonstration over dry slides", "Empathy for the non-technical listener"],
        "cm": ["Using dense jargon without explanation", "Assuming non-technical stakeholders only care about UI colors", "Becoming frustrated when asked simple questions"],
        "fu": ["How did you verify that the evaluator actually understood your concept?", "If a business manager asked 'why not just use ChatGPT directly?', what would you say?"],
        "tags": ["communication", "stakeholders", "presentation", "clarity"]
    },
    {
        "q": "How did you manage source code, branch strategies, and pull requests in your GitHub repository?",
        "sub": "Version Control",
        "d": "Beginner",
        "ans": "Interviewer is assessing: Git workflow, hygiene, and readiness for professional engineering teams. Explain your branching model (e.g., main/staging/feature branches), commit message conventions, PR review requirements, and merge conflict resolution. Illustrative example (replace with your actual project details): 'We adopted a GitHub Flow model: the main branch remained protected and deployable at all times. Every feature or bug fix was developed on a descriptive branch like feature/auth-jwt or fix/db-migration. Before merging, PRs required passing automated GitHub Actions tests and approval from at least one teammate. When conflicts arose, we rebased locally against main before updating the pull request.'",
        "kp": ["Branching strategy (main, feature branches)", "Protected branches and pull request workflows", "Descriptive atomic commit messages", "Merge conflict handling via rebase or merge"],
        "cm": ["Committing directly to main branch", "Vague commit messages like 'fixed stuff' or 'update 2'", "Never using pull requests or peer review in a team setting"],
        "fu": ["What is the difference between git merge and git rebase?", "How did you ensure sensitive environment variables were never accidentally committed?"],
        "tags": ["git", "version-control", "github", "teamwork"]
    },
    {
        "q": "Did your project involve any data collection, cleaning, or preprocessing? How did you ensure data quality?",
        "sub": "Data Preparation",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: data hygiene, preprocessing rigor, and garbage-in-garbage-out awareness. Describe where the raw data came from, common impurities encountered (nulls, duplicates, outliers, formatting discrepancies), the automated cleaning pipeline you implemented, and validation checks applied. Illustrative example (replace with your actual project details): 'We gathered 500 interview questions from academic and placement archives. The raw data contained inconsistencies like mixed case tags, duplicate questions with slight phrasing variations, and empty key points. I wrote an automated ingestion pipeline that parsed the JSON, normalized whitespace, computed SHA-256 hashes of stripped text to block duplicates, and applied token Jaccard similarity to eliminate near-duplicates.'",
        "kp": ["Data sources and raw characteristics", "Handling missing values, duplicates, and outliers", "Automated validation rules and normalization", "Verification of final dataset integrity"],
        "cm": ["Manual copy-pasting without systematic validation", "Ignoring duplicate records or near-duplicates", "Not knowing the distribution or size of your data"],
        "fu": ["How did your pipeline handle corrupted or malformed input records?", "What automated tests verified that data transformations were idempotent?"],
        "tags": ["data-cleaning", "data-quality", "preprocessing", "validation"]
    },
    {
        "q": "How did you handle environment variables, configuration settings, and secrets across development and production?",
        "sub": "Configuration Management",
        "d": "Beginner",
        "ans": "Interviewer is assessing: 12-factor app principles and configuration security. Explain how configuration is separated from code using environment variables, typed settings schemas (e.g., Pydantic BaseSettings), .env file isolation, and production guards against weak default secrets. Illustrative example (replace with your actual project details): 'We adhered to 12-factor principles by loading configurations through Pydantic Settings. In development, settings loaded from a local .env file included in .gitignore. In production, variables like DATABASE_URL and JWT_SECRET_KEY were injected through the hosting platform environment. We added startup validators that refused to start the server in production if JWT_SECRET_KEY was under 32 characters.'",
        "kp": ["Separation of config from code (12-factor app)", "Pydantic Settings / schema validation for env vars", "Secret isolation with .gitignore and template .env.example", "Production startup security validations"],
        "cm": ["Hardcoding secrets, API keys, or database URLs in source code", "Committing .env files to public repositories", "No default validation for missing critical variables"],
        "fu": ["What happens if a required environment variable is missing when the app boots?", "How do you rotate secrets in production without service downtime?"],
        "tags": ["configuration", "secrets", "12-factor", "security"]
    },
    {
        "q": "What research or competitive benchmarking did you conduct before building your project?",
        "sub": "Research & Benchmarking",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: market awareness, analytical research, and deliberate engineering. Explain what existing commercial tools or open-source repositories you studied, their core strengths and deficits, and how your project was uniquely positioned for its intended audience. Illustrative example (replace with your actual project details): 'Before designing our platform, we evaluated existing solutions like LeetCode and generic ChatGPT prompts. While LeetCode is strong for DSA, it offers zero evaluation for HR, behavioral, or Indian campus placement patterns. Conversely, ChatGPT gives generic praise without structured marks or question bank alignment. We identified this gap to build an assessment engine with deterministic rubric scoring and role-specific Indian fresher questions.'",
        "kp": ["Systematic analysis of 2-3 existing solutions", "Identified distinct gaps or unmet user needs", "Informed feature prioritization based on research", "Clear differentiation for target audience"],
        "cm": ["Saying 'no one has ever built anything like this in the world'", "Ignorance of major industry competitors", "Copying a competitor feature-for-feature with no rationale"],
        "fu": ["What is one feature from a competitor that you deliberately chose NOT to build?", "How did your research influence your technical architecture?"],
        "tags": ["research", "benchmarking", "product-strategy", "differentiation"]
    }
]

PART2 = [
    {
        "q": "If you built a RAG (Retrieval-Augmented Generation) chatbot project, how did you handle chunking, embedding, and vector retrieval?",
        "sub": "RAG Architecture",
        "d": "Advanced",
        "ans": "Interviewer is assessing: deep practical knowledge of modern GenAI systems. Explain your document chunking strategy (chunk size and overlap rationale), your embedding model choice, vector database index type, and how you retrieved relevant context into the LLM prompt. Illustrative example (replace with your actual project details): 'For our RAG documentation bot, we chunked PDF manuals using RecursiveCharacterTextSplitter with 500-token chunks and 50-token overlap to preserve semantic continuity. We embedded chunks with BAAI/bge-small-en-v1.5 and stored them in FAISS with cosine similarity. During retrieval, we fetched top-4 chunks, appended them into a system prompt with strict hallucination guardrails, and streamed the answer via Groq.'",
        "kp": ["Chunking strategy (size, overlap, splitting logic)", "Embedding model selection and dimensionality", "Vector database and similarity metric (Cosine/L2)", "Prompt augmentation and hallucination prevention"],
        "cm": ["Using arbitrary chunk sizes with no semantic boundaries", "Not knowing the difference between embedding model and chat model", "Ignoring retrieval evaluation or hallucination risks"],
        "fu": ["What happened when relevant context was split across chunk boundaries?", "How did you handle queries where the knowledge base had no relevant information?"],
        "tags": ["rag", "genai", "vector-db", "embeddings", "llm"]
    },
    {
        "q": "In your RAG chatbot project, how did you measure retrieval quality and reduce hallucinations?",
        "sub": "RAG Evaluation",
        "d": "Advanced",
        "ans": "Interviewer is assessing: empirical evaluation of LLM systems and production safeguards. Discuss RAG evaluation metrics (Faithfulness, Answer Relevance, Context Precision) using frameworks like Ragas or TruLens, prompt engineering constraints, and citation mechanisms. Illustrative example (replace with your actual project details): 'To minimize hallucinations, we instructed the model to answer strictly based on provided context and return \"I do not know based on the provided documents\" when unsure. We evaluated retrieval quality using 50 synthetic Q&A pairs, tracking Context Recall and Faithfulness. Adding a reranker stage using FlashRank increased top-3 context precision by 18%.'",
        "kp": ["Strict negative prompt constraints (\"I do not know\")", "Evaluation metrics: Faithfulness, Context Recall, Precision", "Reranking stage (Cross-Encoder / Cohere / FlashRank)", "Source attribution and citation in outputs"],
        "cm": ["Assuming LLMs never hallucinate if provided a prompt", "No systematic evaluation beyond subjective manual testing", "Unable to define Faithfulness or Context Precision"],
        "fu": ["How do you differentiate between a retrieval failure and a generation failure?", "What role does temperature play in controlling hallucination?"],
        "tags": ["rag", "hallucination", "ragas", "evaluation", "genai"]
    },
    {
        "q": "If you developed an AI Agent project, how did you design tool calling, state management, and loop termination?",
        "sub": "AI Agents",
        "d": "Advanced",
        "ans": "Interviewer is assessing: agentic reasoning loops, tool invocation schemas, and safety controls. Explain the ReAct (Reasoning + Acting) loop, how tool schemas were exposed via JSON Schema / Pydantic, how intermediate state was preserved, and how infinite loops were prevented via maximum iteration bounds. Illustrative example (replace with your actual project details): 'Our research agent used an autonomous ReAct loop. We exposed tools (calculator, search, database query) using Pydantic schemas. The agent inspected user queries, formulated an action plan, called tools, and observed results in memory. We enforced a hard cap of 5 tool calls per turn and implemented schema validation on tool outputs to prevent infinite execution loops.'",
        "kp": ["ReAct / tool-calling workflow", "Structured tool definition via JSON Schema/Pydantic", "State retention across iterative tool steps", "Termination conditions and loop guardrails"],
        "cm": ["Confusing a simple sequential prompt chain with an autonomous agent", "No timeout or iteration limit, risking runaway API costs", "Failing to sanitize or validate tool execution outputs"],
        "fu": ["How did your agent handle a tool execution error gracefully?", "What security controls prevented prompt injection from executing malicious tool calls?"],
        "tags": ["ai-agents", "tool-calling", "react-framework", "llm"]
    },
    {
        "q": "If you built a Machine Learning project, walk me through your feature engineering and data leakage prevention steps.",
        "sub": "ML Engineering",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: ML hygiene, statistical rigor, and feature engineering depth. Explain the features you created from raw data, how you handled categorical variables and missing values, and how you strictly separated training and validation pipelines to prevent data leakage. Illustrative example (replace with your actual project details): 'In our student placement prediction model, we engineered features such as semester-over-semester GPA trajectory and ratio of projects to backlogs. To prevent data leakage, we split data into 80/20 train/test before any imputation or scaling. Imputers and StandardScaler were fit strictly on the training fold and only transformed on test data within an scikit-learn Pipeline.'",
        "kp": ["Domain-specific feature engineering", "Strict train/test separation before transformations", "Use of scikit-learn Pipelines to encapsulate transformers", "Handling of categorical variables and missing values"],
        "cm": ["Fitting scalers or encoders on the entire dataset prior to splitting", "Using future or target-correlated data as input features", "Ignoring multicollinearity between engineered features"],
        "fu": ["How did you verify that your model was not memorizing training data?", "Which single engineered feature contributed highest feature importance?"],
        "tags": ["machine-learning", "feature-engineering", "data-leakage", "pipeline"]
    },
    {
        "q": "In your Machine Learning project, which evaluation metrics did you prioritize and why was accuracy insufficient?",
        "sub": "ML Evaluation",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: metric selection under real-world class distributions. Explain why raw accuracy fails on imbalanced datasets, how you balanced Precision vs Recall based on business costs of False Positives vs False Negatives, and your use of F1-score or PR-AUC. Illustrative example (replace with your actual project details): 'Our disease risk dataset had a 95:5 class imbalance, meaning a dumb classifier predicting all negative achieved 95% accuracy while finding zero patients. We prioritized Recall to minimize False Negatives, ensuring at-risk patients were not missed. We evaluated our model using F1-score and Precision-Recall AUC rather than standard ROC-AUC.'",
        "kp": ["Failure mode of accuracy under class imbalance", "Cost trade-off of False Positives vs False Negatives", "Precision, Recall, F1-score, and PR-AUC definitions", "Threshold tuning based on business impact"],
        "cm": ["Reporting 98% accuracy on a heavily skewed dataset without checking baseline", "Inability to distinguish Precision from Recall", "Not knowing what a confusion matrix shows"],
        "fu": ["What technique did you use to handle the class imbalance (SMOTE, class weights)?", "How did you determine the optimal probability classification threshold?"],
        "tags": ["ml-metrics", "imbalanced-data", "precision-recall", "f1-score"]
    },
    {
        "q": "If you built a Full-Stack Web Application, how did you architect state management and API communication between client and server?",
        "sub": "Full-Stack Architecture",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: end-to-end full-stack cohesion, client state management, and network efficiency. Discuss whether you used TanStack Query, Redux, or Context API, how you cached server responses, managed loading/error states, and structured typed API clients. Illustrative example (replace with your actual project details): 'On the frontend, we used TanStack Query for server state management and React Context for local UI state like active theme. TanStack Query handled automatic background refetching, query deduplication, and optimistic updates. On the backend, FastAPI provided automatic OpenAPI schemas, which we used to generate typed TypeScript interfaces, eliminating type mismatch errors.'",
        "kp": ["Server state (TanStack Query / SWR) vs client UI state", "Cache invalidation and deduplication strategies", "Loading, error, and empty states handling", "Type safety across frontend and backend boundaries"],
        "cm": ["Storing entire server payloads in unstructured useState loops", "Ignoring network failure or offline states in the UI", "Not knowing the difference between client state and server state"],
        "fu": ["How did you prevent unnecessary re-renders in your React component tree?", "How did you implement optimistic UI updates for faster perceived latency?"],
        "tags": ["full-stack", "react", "tanstack-query", "state-management"]
    },
    {
        "q": "If you built a Data Analytics Dashboard project, how did you design the data pipeline and choose visualization charts?",
        "sub": "Analytics & Visualization",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: business intelligence, data aggregation, and visual communication. Describe the pipeline from raw ingestion (CSV/database) to aggregation (SQL/Pandas) and visualization (Power BI/Recharts/Plotly). Explain why specific charts were chosen to answer specific business questions. Illustrative example (replace with your actual project details): 'Our campus placement dashboard processed 5 years of student placement records. We transformed raw university spreadsheets using Pandas into cleaned star-schema tables. We used line charts for historical hiring trends, horizontal bar charts for department median CTC comparisons, and scatter plots for CGPA vs salary correlation. We adhered to clean visual hierarchy without 3D gimmicks.'",
        "kp": ["Data aggregation pipeline (Pandas/SQL star schema)", "Intentional chart selection matched to data types", "Business KPIs clearly emphasized (CTC, placement rate)", "Dashboard visual hierarchy and interactivity"],
        "cm": ["Using pie charts with 20 slices or 3D visual effects", "Describing visuals without knowing the underlying business questions", "Displaying unaggregated raw data that slows down client rendering"],
        "fu": ["What was the most surprising insight discovered through your dashboard?", "How did your dashboard handle filtering across multiple linked dimensions?"],
        "tags": ["data-analytics", "dashboards", "visualization", "power-bi", "kpi"]
    },
    {
        "q": "If you developed a Computer Vision project, how did you handle image preprocessing, model selection, and inference latency?",
        "sub": "Computer Vision",
        "d": "Advanced",
        "ans": "Interviewer is assessing: computer vision pipelines, image augmentation, and edge inference efficiency. Discuss resolution normalization, color space transformations, data augmentation techniques, model architecture (CNN vs YOLO vs MobileNet), and inference frame rates. Illustrative example (replace with your actual project details): 'In our real-time helmet detection system, we resized camera streams to 640x640, normalized pixel values, and used Albumentations for rotation and contrast jittering. We selected YOLOv8-nano over larger variants to maintain 30 FPS on an edge CPU without requiring an expensive GPU. Non-Maximum Suppression (NMS) thresholds were tuned to 0.45 IoU to eliminate duplicate bounding boxes.'",
        "kp": ["Image preprocessing (resizing, normalization, color spaces)", "Data augmentation to prevent overfitting", "Model choice balancing mAP accuracy vs FPS throughput", "Inference optimization (YOLO-nano, ONNX, NMS tuning)"],
        "cm": ["Trying to run massive models on video streams without checking FPS", "Not understanding IoU or Non-Maximum Suppression", "Feeding raw high-resolution images directly into training"],
        "fu": ["How did your model perform under poor lighting or occlusion conditions?", "Did you convert your model to ONNX or TensorRT to optimize inference?"],
        "tags": ["computer-vision", "yolo", "cnn", "image-processing", "deep-learning"]
    },
    {
        "q": "If you developed a Recommendation System project, how did you handle the cold-start problem and user-item sparsity?",
        "sub": "Recommendation Systems",
        "d": "Advanced",
        "ans": "Interviewer is assessing: collaborative vs content-based filtering trade-offs and matrix factorization. Explain how collaborative filtering struggles when new users or items appear (cold start) and how hybrid approaches combine metadata features with interaction matrices to bridge the gap. Illustrative example (replace with your actual project details): 'Our book recommendation engine combined matrix factorization via SVD for users with substantial reading history and content-based cosine similarity on book genres, authors, and synopsis embeddings for new items. For completely new users, we implemented an onboarding questionnaire to collect initial topic preferences, bypassing the cold-start barrier.'",
        "kp": ["Collaborative filtering vs Content-based filtering", "Cold-start problem for new users and new items", "Sparsity handling via matrix factorization (SVD/ALS)", "Hybrid recommendation architecture"],
        "cm": ["Assuming collaborative filtering works on items with zero ratings", "Not measuring recommendation quality beyond offline RMSE", "Ignoring diversity and serendipity in recommendation lists"],
        "fu": ["What evaluation metrics did you use (RMSE, Precision@K, NDCG)?", "How did you prevent the system from creating filter bubbles?"],
        "tags": ["recommendations", "collaborative-filtering", "cold-start", "matrix-factorization"]
    },
    {
        "q": "How did you handle error logging, exception boundaries, and operational monitoring in your backend project?",
        "sub": "Logging & Monitoring",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: observability and production diagnostics. Explain structured logging (JSON format), log severity levels (INFO, WARNING, ERROR), global exception handlers, and correlation request IDs that trace a transaction across system layers. Illustrative example (replace with your actual project details): 'We implemented structured logging using Python\\'s logging module with JSON output formatted for easy parsing. A global FastAPI exception handler caught unhandled exceptions, logged full stack traces with a unique request-id header, and returned clean 500 error messages to the client without leaking internal database traceback details.'",
        "kp": ["Structured logging with consistent log levels", "Global exception handlers preventing server crashes", "Sanitization of error responses (no stack trace leaks)", "Correlation IDs for request tracing"],
        "cm": ["Using print() statements scattered throughout production code", "Swallowing exceptions silently with bare 'except: pass'", "Exposing raw database errors or passwords in client error responses"],
        "fu": ["How would you aggregate logs across multiple distributed servers?", "What metrics would trigger an immediate alert to your engineering team?"],
        "tags": ["logging", "monitoring", "observability", "exception-handling"]
    },
    {
        "q": "How did you design asynchronous background jobs or task processing in your web application?",
        "sub": "Asynchronous Processing",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: understanding of I/O concurrency, message queues, and worker separation. Explain why long-running tasks (email sending, report generation, LLM evaluations) must be offloaded from the main HTTP request-response cycle, and how a worker queue coordinates tasks. Illustrative example (replace with your actual project details): 'In our application, report generation took over 8 seconds. Keeping users waiting on an open HTTP connection risked browser timeouts. We offloaded the job by returning a 202 Accepted response with a task ID, pushing the payload to a Redis queue, and processing it in a background worker process. The frontend polled task status until completion.'",
        "kp": ["Separation of short HTTP requests from long background jobs", "HTTP 202 Accepted pattern with status polling or webhooks", "Message broker role (Redis / RabbitMQ)", "Worker resiliency and retry handling"],
        "cm": ["Executing heavy 10-second processing inside a synchronous HTTP route", "No retry strategy if background task fails mid-execution", "Not understanding the difference between asyncio and multi-process workers"],
        "fu": ["What happens if a worker crashes midway through processing a task?", "How do you prevent duplicate execution of the same background job?"],
        "tags": ["async", "celery", "redis", "background-tasks", "concurrency"]
    },
    {
        "q": "How did you handle pagination, sorting, and search filtering on high-volume database queries?",
        "sub": "Database Optimization",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: query efficiency and database scalability. Contrast offset-based pagination with keyset/cursor-based pagination, explain SQL indexing on sorted columns, and describe full-text or prefix search mechanisms. Illustrative example (replace with your actual project details): 'For our question repository, offset pagination worked well for small page numbers, but OFFSET 50000 degrades performance because PostgreSQL still scans preceding rows. For high-volume tables, we transitioned to cursor-based pagination using the last seen record ID and created a composite index on (category, difficulty, id) to ensure index-only scans.'",
        "kp": ["Offset-limit vs cursor-based pagination trade-offs", "Indexing strategy for combined filtering and sorting", "PostgreSQL ILIKE vs full-text search (tsvector)", "Preventing full table scans on large tables"],
        "cm": ["Running unindexed SELECT * queries with OFFSET 100000", "Fetching all records into Python memory and slicing them in code", "Not providing pagination on endpoints returning dynamic collections"],
        "fu": ["When would you prefer cursor-based pagination over page numbers in UI?", "How does an inverted index speed up text search queries?"],
        "tags": ["pagination", "sql-optimization", "indexing", "search"]
    },
    {
        "q": "How did you manage database connection pooling and prevent connection leaks?",
        "sub": "Database Connections",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: backend resource management and database server health. Explain connection pooling (SQLAlchemy QueuePool), pool size and overflow parameters, contextual session management (context managers), and pool pre-pinging to avoid stale dropped connections. Illustrative example (replace with your actual project details): 'We configured SQLAlchemy\\'s QueuePool with a pool size of 10 and max overflow of 20 to prevent exhausting PostgreSQL connection limits. We ensured all database sessions were managed via context managers or FastAPI dependency injection (get_db) with yield, guaranteeing connections are returned to the pool even when endpoint exceptions occur.'",
        "kp": ["Connection pooling benefits over creating new connections per request", "Pool size, timeout, and max overflow settings", "Guaranteed session cleanup via context managers / finally blocks", "pool_pre_ping to detect disconnected sockets"],
        "cm": ["Creating a new database engine or direct socket connection per HTTP call", "Forgetting to close sessions in error paths, causing pool starvation", "Not knowing PostgreSQL default maximum connection limits (max_connections)"],
        "fu": ["What error message does an application throw when the connection pool is exhausted?", "How does pool_pre_ping work under the hood in SQLAlchemy?"],
        "tags": ["connection-pool", "sqlalchemy", "postgresql", "resource-management"]
    },
    {
        "q": "What third-party APIs or external libraries did you integrate, and how did you isolate your app from their failures?",
        "sub": "API Integration",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: defensive programming and fault tolerance. External APIs can time out, return 500s, or hit rate limits. Discuss timeouts, exponential backoff retries, circuit breakers, and fallback responses to prevent cascading outages. Illustrative example (replace with your actual project details): 'We integrated Groq\\'s API for evaluation. Because external AI endpoints can occasionally throttle or experience latency spikes, we wrapped the HTTP client with a 15-second timeout, tenacity-based exponential backoff for HTTP 429 rate limits, and fallback logic that safely stores candidate answers without losing user input if the API fails.'",
        "kp": ["Strict timeout configurations on all external network calls", "Retry policies with exponential backoff and jitter", "Preserving user state during upstream failures", "Graceful degradation without 500 server crashes"],
        "cm": ["Making network calls without any timeout (hanging indefinitely)", "Infinite immediate retries that exacerbate upstream rate limiting", "Crashing the entire user session when a secondary third-party API fails"],
        "fu": ["What is the difference between a retry mechanism and a circuit breaker?", "How did you test your application\\'s behavior when the third-party API was completely down?"],
        "tags": ["api-integration", "fault-tolerance", "resilience", "retry-pattern"]
    },
    {
        "q": "How did you ensure responsive UI design and cross-device accessibility in your frontend?",
        "sub": "Frontend Accessibility",
        "d": "Beginner",
        "ans": "Interviewer is assessing: UI/UX engineering rigor, mobile responsiveness, and WCAG accessibility awareness. Discuss mobile-first CSS breakpoints, semantic HTML tags, keyboard navigation, color contrast ratios, and screen-reader accessibility (ARIA attributes). Illustrative example (replace with your actual project details): 'We implemented a mobile-first responsive layout using Tailwind CSS breakpoint utilities (sm, md, lg). We used semantic elements (<main>, <nav>, <article>) rather than nested divs, ensured all interactive buttons had aria-labels, and audited contrast ratios with Chrome DevTools to meet WCAG AA standards in both light and dark modes.'",
        "kp": ["Mobile-first responsive design principles", "Semantic HTML elements over generic div tags", "Keyboard focusability and ARIA accessibility", "WCAG AA color contrast compliance"],
        "cm": ["Designing exclusively on a desktop screen and ignoring mobile views", "Using non-semantic clickable elements like <div onClick=...>", "Poor color contrast that makes text unreadable in dark mode"],
        "fu": ["How did you verify accessibility using automated or manual auditing tools?", "How does mobile-first CSS differ from desktop-first CSS?"],
        "tags": ["accessibility", "responsive-design", "frontend", "tailwind", "ui-ux"]
    },
    {
        "q": "How did you handle CORS (Cross-Origin Resource Sharing) between your frontend client and backend server?",
        "sub": "CORS & Networking",
        "d": "Beginner",
        "ans": "Interviewer is assessing: browser security models and HTTP cross-origin protocols. Explain why browsers enforce Same-Origin Policy, how preflight OPTIONS requests work, and how CORS middleware is configured to permit only trusted origin domains in production while allowing localhost in development. Illustrative example (replace with your actual project details): 'Because our React frontend was hosted on port 5173 and FastAPI on 8000, browsers blocked cross-origin fetch requests by default. We added FastAPI\\'s CORSMiddleware, specifying allowed origins from an environment variable. In development, we allowed localhost:5173, while in production we restricted origins strictly to our production domain, preventing unauthorized domains from making credentialed requests.'",
        "kp": ["Same-Origin Policy rationale in browsers", "Preflight HTTP OPTIONS request role", "Explicit allowed origins configuration (avoiding wildcard * with credentials)", "Environment-specific CORS policies"],
        "cm": ["Using allow_origins=[\"*\"] with allow_credentials=True in production", "Assuming CORS is a backend security barrier rather than a browser protection", "Not knowing what constitutes a different origin (protocol, domain, port)"],
        "fu": ["Why does Postman work fine with an API even when CORS fails in Chrome?", "What headers are exchanged during a browser CORS preflight check?"],
        "tags": ["cors", "networking", "browser-security", "http"]
    },
    {
        "q": "How did you manage form state, client-side validation, and feedback errors in your frontend?",
        "sub": "Form Handling",
        "d": "Beginner",
        "ans": "Interviewer is assessing: user input handling, schema validation, and form UX. Explain using React Hook Form with Zod schema validation to eliminate unnecessary component re-renders while providing immediate, inline field-level feedback to users. Illustrative example (replace with your actual project details): 'We used React Hook Form combined with Zod schema resolvers for our registration and onboarding forms. This allowed us to manage form state without re-rendering the entire page on every keystroke. Zod validated email formats, minimum password complexity, and required fields, displaying clean inline error messages before network requests were initiated.'",
        "kp": ["Uncontrolled vs controlled form inputs and re-render optimization", "Schema validation via Zod or Yup", "Immediate inline user feedback before form submission", "Synchronizing client validation with backend validation rules"],
        "cm": ["Submitting invalid forms and relying solely on slow backend error responses", "Re-rendering heavy page trees on every single character keystroke", "Displaying raw JSON error blobs to the end user"],
        "fu": ["Why is client-side validation alone insufficient for web security?", "How did you handle disabled submit buttons during active network requests?"],
        "tags": ["forms", "react-hook-form", "zod", "validation", "frontend"]
    },
    {
        "q": "Did you implement any caching layer in your project, and how did you handle cache invalidation?",
        "sub": "Caching Strategies",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: caching patterns and cache consistency. Discuss in-memory caching (lru_cache) or distributed caching (Redis), cache keys, TTL (Time-to-Live) expiration, and explicit cache invalidation when records are updated or deleted. Illustrative example (replace with your actual project details): 'We cached static reference questions and rubric definitions in Redis using a key format of questions:{category}:{id} with a 1-hour TTL. When an admin updated or soft-deleted a question via the admin API, we explicitly invalidated the corresponding Redis cache key and cleared category list caches, ensuring users never saw stale data.'",
        "kp": ["Cache-aside (read-through) pattern", "TTL-based expiration vs event-driven invalidation", "Consistent and descriptive cache key naming conventions", "Cache stampede prevention basics"],
        "cm": ["Caching data indefinitely without any TTL or invalidation mechanism", "Caching user-specific or sensitive data in shared public caches", "Assuming caching solves poorly indexed database queries"],
        "fu": ["What is the difference between Cache-Aside and Write-Through caching?", "What happens during a cache stampede and how do you mitigate it?"],
        "tags": ["caching", "redis", "performance", "architecture"]
    },
    {
        "q": "How did you design your project so that it could be easily handed over to another developer?",
        "sub": "Documentation & Maintainability",
        "d": "Beginner",
        "ans": "Interviewer is assessing: engineering empathy, code documentation, and team professionalism. Discuss comprehensive README setup guides, Docker one-command spinups, docstrings, type annotations, and automated API documentation (Swagger/OpenAPI). Illustrative example (replace with your actual project details): 'We structured the repository so a new developer could run docker compose up --build after copying .env.example. We wrote clean README documentation with prerequisite listings, step-by-step local setup, and testing commands. All backend endpoints were typed with Pydantic and auto-generated Swagger UI docs at /docs with sample payloads.'",
        "kp": ["One-command setup via Docker or automated scripts", "Clear README with architecture overview and prerequisite list", "Type hints and self-documenting code", "Auto-generated OpenAPI / Swagger documentation"],
        "cm": ["No README or outdated setup instructions that fail on fresh machines", "Hardcoded absolute file paths tied to a personal laptop", "Undocumented environment variables required for startup"],
        "fu": ["If a new teammate joined tomorrow, what would be their biggest hurdle in understanding your code?", "How do you decide between writing inline comments versus refactoring code for readability?"],
        "tags": ["documentation", "maintainability", "docker", "onboarding"]
    },
    {
        "q": "What was the most rewarding moment during your project journey, and what did you learn about yourself as an engineer?",
        "sub": "Reflection & Growth",
        "d": "Beginner",
        "ans": "Interviewer is assessing: passion, grit, and professional self-reflection. Share a genuine milestone—such as the first time an end-to-end flow worked, seeing a real user test the product successfully, or solving a stubborn bug after days of debugging—and reflect on how it shaped your engineering work ethic. Illustrative example (replace with your actual project details): 'The most rewarding moment was seeing a junior batchmate complete an entire mock interview session and receive structured feedback that helped them correct a vague answer. It transformed code from an abstract assignment into a tool that genuinely helped someone. It taught me that I am driven by building practical, working software that delivers verifiable user value.'",
        "kp": ["Specific, memorable engineering milestone", "Shift from theoretical code to user impact", "Self-awareness about personal motivation and engineering drive", "Authentic and humble tone"],
        "cm": ["Saying 'getting an A grade from the professor' as the sole reward", "Sounding detached or indifferent about your own project", "Exaggerating emotional reactions"],
        "fu": ["How has this project influenced the kinds of engineering roles you are targeting?", "What habit did you form during this project that you carry into your next codebase?"],
        "tags": ["reflection", "growth", "motivation", "engineering-mindset"]
    }
]

PART3 = [
    {
        "q": "How did you manage software dependencies and ensure reproducibility across different developer machines?",
        "sub": "Dependency Management",
        "d": "Beginner",
        "ans": "Interviewer is assessing: environment isolation and build reproducibility. Discuss pinned requirements files (requirements.txt, package-lock.json), virtual environments (venv), multi-stage Docker builds, and keeping dev dependencies separate from production dependencies. Illustrative example (replace with your actual project details): 'We pinned all production dependencies with exact versions in requirements.txt and maintained a separate requirements-dev.txt for test tools like pytest and httpx. For the frontend, package-lock.json was strictly committed. Docker containers ensured that the exact same Python 3.12 and Node 22 runtime ran identically on Windows, Linux, and macOS.'",
        "kp": ["Version pinning in package manifests", "Separation of production and dev dependencies", "Lock files committed to version control", "Containerization for OS-level runtime consistency"],
        "cm": ["Unpinned dependencies that break builds when libraries update", "Committing virtual environments (node_modules, .venv) to Git", "Ignoring lock files during builds"],
        "fu": ["What is the danger of using unpinned dependencies in production?", "How does package-lock.json differ from package.json?"],
        "tags": ["dependencies", "docker", "reproducibility", "python"]
    },
    {
        "q": "In your full-stack application, how did you handle user session expiry, token refresh, and logout?",
        "sub": "Session Management",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: security architecture and authentication lifecycles. Explain short-lived JWT access tokens (15-30 minutes) combined with long-lived refresh tokens (7-14 days), silent token refresh via Axios/fetch interceptors, and secure token clearing on logout. Illustrative example (replace with your actual project details): 'We implemented a dual-token strategy. The access token had a 30-minute expiry, while the refresh token was stored securely and valid for 14 days. An HTTP interceptor on the frontend caught 401 Unauthorized responses, paused queued requests, called /api/v1/auth/refresh to retrieve a fresh token pair, and replayed the original requests seamlessly without interrupting the user.'",
        "kp": ["Dual-token architecture (short-lived access + long-lived refresh)", "HTTP interceptors for seamless token renewal", "Secure storage considerations (memory vs HTTP-only cookies)", "Proper cleanup and invalidation upon logout"],
        "cm": ["Generating access tokens with 1-year expiration to avoid refresh logic", "Forgetting to clear tokens on logout", "Infinite 401 retry loops that hang the frontend"],
        "fu": ["Why should access tokens be short-lived?", "How would you revoke a refresh token if a user's device is compromised?"],
        "tags": ["auth", "jwt", "refresh-token", "security"]
    },
    {
        "q": "How did you design database transactions to prevent partial updates and data corruption?",
        "sub": "Data Integrity",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: ACID properties and transactional integrity in database applications. Discuss wrapping multi-table writes in atomic transactions, automatic rollbacks on exceptions, and database-level constraints. Illustrative example (replace with your actual project details): 'When finalizing an interview session, we needed to update the session status to \"completed\", persist the synthesized performance report, and update user practice analytics. We wrapped all three operations inside a single SQLAlchemy session transaction block. If an error occurred during analytics aggregation, the entire transaction rolled back cleanly, preventing half-saved session states.'",
        "kp": ["Atomicity in multi-statement database operations", "Automatic rollback on failure via context managers", "ACID principles applied in practice", "Database-level constraints (foreign keys, uniqueness)"],
        "cm": ["Committing individual database writes separately inside a loop", "Leaving database sessions in an uncommitted dirty state after exceptions", "Ignoring transactional integrity for multi-step workflows"],
        "fu": ["What is the difference between database commit and flush in SQLAlchemy?", "How does an isolation level like Read Committed prevent dirty reads?"],
        "tags": ["database", "acid", "transactions", "sqlalchemy"]
    },
    {
        "q": "How did you design your frontend component hierarchy to maximize reusability and maintainability?",
        "sub": "Component Architecture",
        "d": "Beginner",
        "ans": "Interviewer is assessing: React composition, modular design, and props hygiene. Explain separating presentation components (Buttons, Badges, Modals) from container/page components (Dashboard, InterviewRoom), using TypeScript interfaces for props, and avoiding prop drilling. Illustrative example (replace with your actual project details): 'We structured our frontend into atomic UI primitives (Card, Badge, Button, Modal) housed in a components/ui directory, while feature-specific logic lived in views. All components had strongly-typed TypeScript prop contracts. We avoided deep prop drilling by utilizing React Context for global state and custom hooks for API calls.'",
        "kp": ["Separation of presentation and business logic components", "Strongly-typed prop interfaces with TypeScript", "Composition over inheritance", "Custom hooks for encapsulated stateful logic"],
        "cm": ["Building massive 1000-line monolithic components", "Copy-pasting identical button or card code across 10 pages", "Excessive prop drilling through 5 levels of components"],
        "fu": ["When do you choose a custom hook over standard inline state?", "How do you balance component reusability with over-engineering?"],
        "tags": ["react", "components", "frontend-architecture", "typescript"]
    },
    {
        "q": "What was your strategy for handling slow networks or loading spinners in your frontend application?",
        "sub": "User Experience",
        "d": "Beginner",
        "ans": "Interviewer is assessing: UX polish, perceived performance, and visual stability. Discuss skeleton loaders instead of jarring spinners, disabled button states during submission, optimistic updates, and clean empty states when collections have zero items. Illustrative example (replace with your actual project details): 'Instead of jarring full-screen spinners that cause layout shifts, we designed SVG skeleton cards matching our question library layout. While evaluations were processing, we displayed animated progress pulses and disabled submission buttons to prevent double-clicks. When search filters yielded zero results, we showed an illustrative empty state with a \"Clear Filters\" action.'",
        "kp": ["Skeleton loaders to prevent Cumulative Layout Shift (CLS)", "Disabled states and spinner indicators on submit buttons", "Clear empty states with recovery actions", "Graceful timeout and error retry alerts"],
        "cm": ["Leaving users staring at blank white screens with no loading feedback", "Allowing users to submit forms multiple times by spamming buttons", "Ignoring empty state design when no data is returned"],
        "fu": ["What is Cumulative Layout Shift and why does it harm user experience?", "How did you test your frontend UI under simulated slow 3G network conditions?"],
        "tags": ["ux", "loading-states", "skeletons", "frontend"]
    },
    {
        "q": "How did you sanitize and validate user-submitted inputs to prevent injection attacks and XSS?",
        "sub": "Input Validation",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: defense-in-depth security principles. Explain validating types, lengths, and regex patterns at the API boundary using Pydantic, parameterized SQL queries via ORMs to eliminate SQL injection, and proper escaping in React JSX to prevent Cross-Site Scripting (XSS). Illustrative example (replace with your actual project details): 'We enforced strict input boundaries using Pydantic models with min/max length constraints and regex patterns for IDs. Because SQLAlchemy uses parameterized queries, user inputs are never concatenated directly into raw SQL strings, neutralizing SQL injection. On the frontend, React\\'s JSX engine automatically escapes string values before rendering, preventing script tag injection.'",
        "kp": ["Boundary validation with Pydantic schemas", "Parameterized queries preventing SQL injection", "Automatic context-aware escaping in modern frameworks", "Denial-of-Service prevention via payload size limits"],
        "cm": ["Concatenating raw user strings into SQL queries", "Using dangerouslySetInnerHTML without sanitization", "Trusting user input without length or type checks"],
        "fu": ["How could a malicious user execute SQL injection in an improperly written raw query?", "What is dangerouslySetInnerHTML in React and when is it safe to use?"],
        "tags": ["security", "sql-injection", "xss", "input-validation"]
    },
    {
        "q": "If you built an AI application, how did you manage prompt templates and prevent prompt injection attacks?",
        "sub": "Prompt Security",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: prompt engineering rigor and GenAI vulnerability mitigation. Discuss separating system instructions from user inputs using structured delimiter tags, validating inputs before interpolation, and enforcing strict JSON output schemas. Illustrative example (replace with your actual project details): 'We isolated system instructions from user-submitted answers by encapsulating candidate answers inside explicit XML delimiters (<user_answer>...</user_answer>) in the prompt. We instructed the LLM to treat content within delimiters strictly as text to be graded rather than executable directives. Furthermore, we enforced structured JSON output validation via Pydantic, so any injection attempting conversational hijacking was rejected.'",
        "kp": ["System prompt vs user input boundary separation", "Use of delimiters (<context>, XML tags)", "Structured schema enforcement (Pydantic / Instructor)", "Defensive instructions against role hijacking"],
        "cm": ["Direct f-string concatenation of raw user input without boundaries", "Assuming LLMs can never be fooled by prompt injection", "Allowing LLM unstructured responses to dictate application control flow"],
        "fu": ["What is an indirect prompt injection attack?", "How do you test your prompt's resilience against jailbreak attempts?"],
        "tags": ["prompt-engineering", "prompt-injection", "genai", "security"]
    },
    {
        "q": "How did you monitor and optimize LLM token usage and API latency in your AI system?",
        "sub": "LLM Optimization",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: financial and performance awareness in AI systems. Discuss tracking prompt tokens, completion tokens, latency in milliseconds, caching evaluations for identical inputs, and selecting appropriately sized models. Illustrative example (replace with your actual project details): 'We logged prompt_tokens, completion_tokens, and latency_ms for every evaluation turn in our database. By analyzing these logs, we pruned verbose few-shot examples from the system prompt, reducing token consumption by 35% per turn without degrading evaluation accuracy. We also utilized Groq\\'s Llama 3.3 70B versatile model, achieving sub-second inference latencies.'",
        "kp": ["Token accounting (input vs output tokens)", "Latency tracking in milliseconds per request", "Prompt pruning to cut redundant overhead", "Model selection matched to task complexity"],
        "cm": ["Ignoring token usage and discovering massive API bills", "Sending entire document histories unnecessarily on every turn", "No latency instrumentation or timeout thresholds"],
        "fu": ["Why are completion tokens significantly slower and more expensive than prompt tokens?", "How did you balance prompt brevity with grading detail?"],
        "tags": ["llm", "tokens", "latency", "groq", "optimization"]
    },
    {
        "q": "How did you handle database schema migrations across different versions of your application?",
        "sub": "Database Migrations",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: schema versioning and deployment safety. Explain migration tools (Alembic), generating versioned migration scripts, upgrading schemas automatically during container startup, and supporting rollback downgrades. Illustrative example (replace with your actual project details): 'We managed database schema evolution using Alembic. Every change to our SQLAlchemy models generated an autocompiled, reviewed revision script in alembic/versions. During deployment, the container entrypoint ran alembic upgrade head before launching Uvicorn. This eliminated manual ALTER TABLE commands and guaranteed identical schemas across all environments.'",
        "kp": ["Version-controlled migration files in Git", "Automated forward migrations during container startup", "Rollback capability via downgrade scripts", "Preventing drift between Python models and database tables"],
        "cm": ["Manually running ALTER TABLE queries in production DB consoles", "Dropping and recreating tables on every schema change, losing user data", "Not testing migration scripts on clean databases"],
        "fu": ["What precautions must you take when adding a NOT NULL column to an existing table with data?", "How does Alembic track which migrations have already run on a database?"],
        "tags": ["alembic", "migrations", "postgresql", "database"]
    },
    {
        "q": "How did you ensure that your code conformed to standard code quality, formatting, and linting rules?",
        "sub": "Code Quality",
        "d": "Beginner",
        "ans": "Interviewer is assessing: professional coding discipline and automated code style enforcement. Discuss tools like Ruff, Black, Flake8, ESLint, and Prettier, along with pre-commit hooks that catch formatting and import errors before code reaches remote repositories. Illustrative example (replace with your actual project details): 'We enforced PEP 8 standards using Ruff for Python backend linting and Prettier with ESLint for frontend TypeScript formatting. We configured pre-commit hooks that automatically checked for unused imports, formatting discrepancies, and syntax errors prior to commit creation, ensuring clean Git diffs.'",
        "kp": ["Automated linting and formatting tools (Ruff, ESLint)", "PEP 8 standards and TypeScript strict mode", "Pre-commit hooks and CI lint checks", "Clean, readable, maintainable diffs"],
        "cm": ["Inconsistent indentation and mixed tabs/spaces across files", "Committing commented-out dead code blocks", "Disabling all linter rules rather than fixing clean code issues"],
        "fu": ["What is the difference between a linter and a formatter?", "Why is keeping Git diffs minimal and clean important in team environments?"],
        "tags": ["linting", "code-quality", "ruff", "eslint", "formatting"]
    },
    {
        "q": "In a data-intensive project, how did you handle large datasets that could not fit comfortably into RAM?",
        "sub": "Large Data Processing",
        "d": "Advanced",
        "ans": "Interviewer is assessing: memory management and streaming data processing. Discuss chunked iteration (Pandas chunksize, generator functions), database-side filtering and aggregation, and memory-efficient column types. Illustrative example (replace with your actual project details): 'When processing a 4GB dataset on an 8GB machine, loading the entire CSV into Pandas caused out-of-memory errors. We refactored the ingestion pipeline to read files in 10,000-row chunks using pd.read_csv(..., chunksize=10000) and generator functions, yielded processed aggregates, and committed batched records to PostgreSQL. This stabilized memory consumption at under 250MB throughout execution.'",
        "kp": ["Chunked reading and processing of large files", "Generator functions for lazy stream evaluation", "Database-level aggregations over in-memory Python loops", "Downcasting numeric types to save memory"],
        "cm": ["Attempting to read massive files with pd.read_csv() all at once", "Ignoring Out-Of-Memory crashes", "Not knowing how Python generators save memory"],
        "fu": ["How do generator functions using 'yield' differ from standard list functions?", "When would you transition from Pandas chunks to Polars or Apache Spark?"],
        "tags": ["big-data", "memory-management", "generators", "pandas", "optimization"]
    },
    {
        "q": "How did you design authentication middleware or guards to protect private API routes?",
        "sub": "Route Protection",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: security architecture and dependency injection. Explain how FastAPI dependency injection (get_current_user) intercepts requests, parses the Authorization header, validates the JWT token signature and expiration, queries the user, and rejects unauthenticated requests with 401 Unauthorized before route handlers execute. Illustrative example (replace with your actual project details): 'We secured protected routes using FastAPI\\'s Depends(get_current_user). The dependency extracted the Bearer token, decoded the JWT signature using our secret key, checked expiration, and retrieved the active User from the database. Protected endpoints simply injected current_user: CurrentUser, guaranteeing that unauthenticated requests were intercepted at the boundary.'",
        "kp": ["Reusable dependency injection for route protection", "Bearer token extraction from HTTP Authorization header", "Cryptographic signature and expiry verification", "Role-based access control (AdminUser vs StandardUser)"],
        "cm": ["Copying JWT verification code manually inside every single endpoint handler", "Not checking if the decoded user is marked active in the database", "Returning 403 Forbidden instead of 401 Unauthorized for missing tokens"],
        "fu": ["What is the exact semantic difference between 401 Unauthorized and 403 Forbidden?", "How did you implement role-based access control for admin endpoints?"],
        "tags": ["fastapi", "auth-guards", "jwt", "middleware"]
    },
    {
        "q": "How did you prevent race conditions or duplicate record creation during concurrent requests in your project?",
        "sub": "Concurrency & Integrity",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: concurrent data integrity and database constraints. Explain unique database indexes, optimistic locking, or atomic upsert statements (ON CONFLICT DO UPDATE) to prevent race conditions that application-level checks fail to catch. Illustrative example (replace with your actual project details): 'In our question import feature, checking if a question exists in Python before inserting creates a race condition if two admins import concurrently. To ensure atomicity, we created a unique database constraint on question_hash and used PostgreSQL\\'s INSERT ... ON CONFLICT (question_hash) DO NOTHING. This pushed concurrency enforcement to the database engine where it is guaranteed atomic.'",
        "kp": ["Unique constraints at the database level", "Atomic upserts (ON CONFLICT DO UPDATE/NOTHING)", "Flaw of check-then-act application logic under concurrency", "Database locks and isolation levels"],
        "cm": ["Relying solely on Python if not db.query(...) before saving", "Not handling unique constraint integrity errors", "Assuming low traffic means concurrency never happens"],
        "fu": ["What is a race condition in a web application?", "How does an atomic database transaction prevent double-spending or duplicate submissions?"],
        "tags": ["concurrency", "race-conditions", "database-constraints", "integrity"]
    },
    {
        "q": "How did you design your frontend styling architecture to maintain visual consistency without bloated CSS?",
        "sub": "CSS Architecture",
        "d": "Beginner",
        "ans": "Interviewer is assessing: design system implementation and maintainable CSS. Discuss utility-first styling with Tailwind CSS, design tokens (color palette, spacing scales, typography), theme variables, and keeping arbitrary inline styles minimal. Illustrative example (replace with your actual project details): 'We built our design system with Tailwind CSS using a curated palette of semantic tokens (primary, surface, border, muted). We declared dark mode classes using Tailwind\\'s class strategy and CSS variables, ensuring consistent contrast across light and dark themes. We avoided arbitrary magic numbers, sticking strictly to Tailwind\\'s spacing scale for layout harmony.'",
        "kp": ["Curated design tokens (colors, typography, spacing)", "Utility-first CSS architecture with Tailwind", "Dark and light mode theming via CSS variables", "Consistency without bloated custom CSS stylesheets"],
        "cm": ["Hardcoding random hex codes and arbitrary pixel margins everywhere", "Writing massive monolithic CSS files with high specificity conflicts", "Inconsistent font sizes and button styles across pages"],
        "fu": ["What are the benefits of utility CSS over traditional BEM methodology?", "How did you purge unused CSS classes in production builds?"],
        "tags": ["tailwind", "css", "design-system", "theming", "frontend"]
    },
    {
        "q": "How did you ensure that client-side routing, navigation, and protected pages worked seamlessly in your SPA?",
        "sub": "Client Routing",
        "d": "Beginner",
        "ans": "Interviewer is assessing: Single Page Application navigation and route guards. Explain React Router setup, nested layouts, protected route wrappers that redirect unauthenticated users to /login while preserving target destination, and handling 404 Not Found pages. Illustrative example (replace with your actual project details): 'We managed routing using React Router v6 with nested layout structures. We created a ProtectedRoute wrapper that evaluated authentication status from our AuthContext. If an unauthenticated user tried to access /dashboard, they were redirected to /login with state={{ from: location }}, allowing seamless redirection back to their intended page upon successful login.'",
        "kp": ["Declarative routing with React Router", "Protected route wrappers and authentication redirection", "Preserving target destination on login redirect", "Catch-all 404 routes and clean URL structures"],
        "cm": ["Flickering protected content briefly before redirecting to login", "Losing user destination after login redirect", "Not handling 404 routes gracefully"],
        "fu": ["How does client-side routing in an SPA differ from traditional server-side page navigation?", "How did you configure your production web server (Nginx/Vercel) to handle SPA deep-linking?"],
        "tags": ["react-router", "spa", "navigation", "route-guards"]
    },
    {
        "q": "What automated continuous integration (CI) checks did you set up for your project repository?",
        "sub": "Continuous Integration",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: DevOps automation and quality gates. Explain GitHub Actions workflows that trigger on pull requests, running linting checks, type checking, and automated test suites against a test database before code can be merged into main. Illustrative example (replace with your actual project details): 'We created a GitHub Actions CI workflow triggered on every pull request to main. The workflow spun up Python 3.12 and Node 22 runners, ran Ruff linting and TypeScript tsc type checks, and executed our pytest test suite against in-memory SQLite. Pull requests were blocked from merging unless all CI status checks passed green.'",
        "kp": ["GitHub Actions workflow configuration (.github/workflows/ci.yml)", "Parallel checks: linting, type validation, unit tests", "Blocking merges on failing pull request status checks", "Fast feedback loop for developers"],
        "cm": ["Relying solely on local 'it works on my machine' claims", "Running tests manually right before presentation", "Ignoring failing CI badges on GitHub"],
        "fu": ["How do you prevent flaky tests from breaking your CI pipeline?", "What is the difference between Continuous Integration and Continuous Deployment?"],
        "tags": ["ci-cd", "github-actions", "devops", "automation"]
    },
    {
        "q": "How did you ensure that your code adhered to clean code principles such as DRY, SOLID, and separation of concerns?",
        "sub": "Clean Code",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: software craftsmanship and architectural discipline. Explain Single Responsibility (separating route handlers from database business logic in service files), DRY (reusable utility functions and schemas), and Dependency Inversion. Illustrative example (replace with your actual project details): 'We structured our backend into distinct layers: routes handled HTTP parameters and validation, services contained core business and evaluation logic, and models defined database schemas. This Single Responsibility Principle ensured routes remained lean. We adhered to DRY by centralizing rubric calculation logic into a shared validator rather than repeating it across endpoints.'",
        "kp": ["Separation of concerns (Routes, Services, Models)", "Single Responsibility Principle (SRP) applied in practice", "DRY principle through shared helper utilities", "High cohesion and low coupling"],
        "cm": ["Putting 500 lines of database queries and business logic directly in route functions", "Duplicating identical validation logic across multiple files", "Confusing theoretical SOLID definitions without code examples"],
        "fu": ["Can you give an example of a refactoring where you separated business logic from an HTTP route?", "When does following DRY too dogmatically lead to premature abstraction?"],
        "tags": ["clean-code", "solid-principles", "architecture", "refactoring"]
    },
    {
        "q": "How did you benchmark the cold-start and warm-start latency of your application or APIs?",
        "sub": "Latency Benchmarking",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: empirical performance testing and initialization costs. Explain measuring the time taken for the initial application boot and first request (cold start: importing modules, establishing database pools) versus steady-state subsequent requests (warm start), using tools like curl, Apache Bench, or Locust. Illustrative example (replace with your actual project details): 'We benchmarked API latency using curl -w format flags. The cold-start request took 480ms due to SQLAlchemy connection pool initialization and model schema caching. Subsequent warm requests averaged 22ms for database lookups and 650ms for Groq AI inference. This confirmed that our steady-state latency was well within acceptable thresholds.'",
        "kp": ["Cold start (process boot, connection initialization) vs warm start", "Measurement tools (curl, ab, custom middleware timers)", "Identifying initialization overheads", "Target latency SLAs for interactive user experiences"],
        "cm": ["Assuming cold start and warm start have identical performance", "Measuring latency only in browser DevTools with network throttling on", "No quantitative latency numbers to share"],
        "fu": ["How would you minimize container cold-start latency in serverless environments?", "What percentage of your warm-start response time was spent in database queries versus network transit?"],
        "tags": ["benchmarking", "latency", "cold-start", "performance"]
    },
    {
        "q": "How did you handle user feedback, usability testing, and iteration on your project's interface?",
        "sub": "User Feedback",
        "d": "Beginner",
        "ans": "Interviewer is assessing: user-centric engineering and feedback responsiveness. Describe conducting informal usability testing with classmates or peers, observing where they hesitated or encountered confusion, and iterating on the UI/UX based on real observations. Illustrative example (replace with your actual project details): 'We conducted user testing sessions with 8 fellow engineering students. We noticed that several users were confused about whether their voice was being recorded during mock interview sessions. Based on this direct feedback, we added an active audio waveform visualizer and an explicit recording status badge, immediately increasing candidate confidence during practice.'",
        "kp": ["User testing sessions conducted with real target audience", "Specific user friction point observed", "Direct design iteration implemented in response", "Verifiable improvement in user comprehension"],
        "cm": ["Assuming the developer knows what users want without testing", "Dismissing user feedback as 'user error'", "No changes made between initial prototype and final product"],
        "fu": ["What was the most surprising piece of feedback you received from a test user?", "How do you decide which user requests to build versus ignore?"],
        "tags": ["user-feedback", "usability", "ux", "iteration"]
    },
    {
        "q": "Looking back, what is the most important technical skill or concept you learned from building this project?",
        "sub": "Technical Growth",
        "d": "Beginner",
        "ans": "Interviewer is assessing: learning agility and intellectual curiosity. Choose a specific modern technical skill—such as asynchronous programming, database indexing, TypeScript type systems, or GenAI prompt engineering—and explain how hands-on implementation gave you a much deeper understanding than passive coursework. Illustrative example (replace with your actual project details): 'The most impactful skill I mastered was building reliable production systems around probabilistic LLM APIs. In university classes, APIs always return deterministic results. Building this platform taught me how to write robust validation layers with Pydantic, handle timeouts and retries defensively, and ground AI with domain rubrics so the system remains consistent and dependable.'",
        "kp": ["Specific, advanced technical skill identified", "Contrast between theoretical coursework and practical implementation", "Engineering maturity and problem-solving growth", "Enthusiasm for software craft"],
        "cm": ["Giving a generic answer like 'I learned Python'", "Sounding like building the project was just an unpleasant chore", "Failing to explain how the skill was applied in practice"],
        "fu": ["What technical concept are you currently exploring or learning next?", "How will this skill accelerate your impact in your first 90 days on our engineering team?"],
        "tags": ["growth", "learning", "engineering-mindset", "fresher"]
    }
]

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    f1 = OUT_DIR / "01.json"
    f2 = OUT_DIR / "02.json"
    f3 = OUT_DIR / "03.json"
    f1.write_text(json.dumps(PART1, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    f2.write_text(json.dumps(PART2, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    f3.write_text(json.dumps(PART3, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(PART1)} to 01.json, {len(PART2)} to 02.json, {len(PART3)} to 03.json (Total: {len(PART1) + len(PART2) + len(PART3)})")

if __name__ == "__main__":
    main()
