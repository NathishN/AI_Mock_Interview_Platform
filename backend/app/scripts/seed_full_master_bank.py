"""Comprehensive Master Interview Question Bank Seeder
Builds and inserts all distinct questions from Parts 1 through 12 across:
- Part 1: Self-Intro & HR
- Part 2: Resume, Projects & Internships
- Part 3: Coding (Strings, Numbers, Arrays, Python)
- Part 4: Python Internals
- Part 5: Java & Object-Oriented Programming
- Part 6: SQL & Databases
- Part 7: Git, GitHub & CI/CD
- Part 8: Web Development (Frontend, Backend, APIs, Supabase)
- Part 9: AI, ML, Deep Learning, GenAI, RAG & Agents
- Part 10: Networking, Cybersecurity & IoT
- Part 11: Company-Specific Profiles (IBM, Hexaware, Payoda, SWS AI, AquaAirX, Wheelson)
- Part 12: Questions for the Interviewer
"""

import logging
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.question import Question, question_fingerprint
from app.schemas.question import QuestionCreate

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("seed_full_master_bank")

QUESTIONS = [
    # ---------------- PART 1: HR & BACKGROUND ----------------
    {
        "q": "Tell me about your family background.",
        "cat": "HR", "sub": "Personal Background", "d": "Beginner", "type": "hr",
        "roles": ["Software Development Engineer", "AI Engineer"], "stages": ["HR"],
        "ans": "Interviewers ask about your family background to understand your roots, values, stability, and support system. Structure your answer: 1) Number of members in your immediate family, 2) Parents' professions and the core work values they instilled in you (discipline, honesty, hard work), 3) Sibling information if applicable, 4) Brief conclusion highlighting their support for your education. Illustrative example: 'We are a close-knit family of four from Coimbatore. My father is an electrical contractor who taught me the value of systematic troubleshooting and persistence, while my mother is a high school mathematics teacher who inspired my love for logic and analytical problem-solving. My elder sister works as a software developer, which gave me an early appreciation for technology. My family has always supported my academic and engineering goals.'",
        "kp": ["Keep it concise, respectful, and positive (under 60 seconds)", "Focus on values learned: work ethic, perseverance, and curiosity", "Transition smoothly back to your career focus"],
        "crit": ["Warm, respectful tone and clear articulation", "Avoid overly personal or confidential details"],
        "cm": ["Giving an excessively long history of extended relatives", "Complaining about family financial or personal difficulties during an HR round"],
        "fu": ["How has your family influenced your decision to enter engineering?", "Does your family support your relocation to another city?"],
        "tags": ["master-bank", "ibm", "hexaware", "hr", "personal-background"]
    },
    {
        "q": "Why did you choose your college?",
        "cat": "HR", "sub": "College Choice", "d": "Beginner", "type": "hr",
        "roles": ["Software Development Engineer", "AI Engineer"], "stages": ["HR"],
        "ans": "Interviewers assess how deliberately you make major life decisions. Highlight: 1) Institutional reputation for academic rigor and engineering labs, 2) Vibrant coding clubs, hackathon participation, and technical symposiums, 3) Faculty mentorship and alumni network, 4) Campus placement record and industry partnerships. Illustrative example: 'I chose my college because of its strong laboratory infrastructure and active technical community. During my admission research, I noticed that students regularly participated in national hackathons and open-source events. The college's emphasis on hands-on project work rather than pure textbook memorization aligned with my goal of becoming a practical software engineer.'",
        "kp": ["Highlight proactive decision making based on labs and technical culture", "Emphasize participation in hackathons, clubs, and practical learning", "Maintain a positive, appreciative attitude toward your alma mater"],
        "crit": ["Clear, rational explanation of college selection criteria", "Evidence of maximizing opportunities available on campus"],
        "cm": ["Saying 'I got this college through government counseling, I had no choice'", "Disparaging your college or faculty"],
        "fu": ["What was the most impactful campus initiative or club you took part in?", "If you could change one thing about your college curriculum, what would it be?"],
        "tags": ["master-bank", "hexaware", "ibm", "hr", "college"]
    },
    {
        "q": "Are you willing to relocate, work night shifts, or work in US time zones?",
        "cat": "Company & Workplace", "sub": "Flexibility & Relocation", "d": "Beginner", "type": "hr",
        "roles": ["Software Development Engineer", "AI Engineer", "Support Engineer"], "stages": ["HR"],
        "ans": "This is a critical operational check across IT service firms (Hexaware, TCS, IBM) and global startups. Interviewers need unambiguous assurance that you can adapt to client deadlines, distributed team timezones, and corporate location transfers. Strategy: 1) Give an enthusiastic, unconditional 'Yes', 2) Explain why: as a fresher, maximizing learning exposure, collaborating directly with global teams, and experiencing different engineering hubs accelerates career growth, 3) Mention prior adaptability (e.g., adapting to hostel life or managing late-night project deadlines). Illustrative example: 'Yes, absolutely. I am 100% willing to relocate to any company office location and work in night shifts or US overlapping timezones as required by client deliverables. In my early career, my priority is maximum learning, working with experienced global colleagues, and delivering value to our clients, so flexibility with location and working hours comes naturally to me.'",
        "kp": ["Unambiguous, positive confirmation without hesitation", "Frame flexibility as an opportunity for rapid career acceleration and global exposure", "Assure the recruiter of family alignment with relocation"],
        "crit": ["High energy, genuine willingness, and professional maturity", "No conditional reservations or reluctant undertones"],
        "cm": ["Hesitating or saying 'Only if my parents agree' or 'Only if I get my home city'", "Asking immediately about shift allowances in an aggressive tone"],
        "fu": ["How do you ensure healthy sleep and productivity when transitioning between day and night shifts?", "How soon would you be able to relocate once the offer is confirmed?"],
        "tags": ["master-bank", "hexaware", "ibm", "company-workplace", "relocation", "shifts", "top-30"]
    },
    {
        "q": "Are you aware of the service agreement or bond, and are you comfortable with it?",
        "cat": "Company & Workplace", "sub": "Service Agreement & Commitment", "d": "Beginner", "type": "hr",
        "roles": ["Software Development Engineer", "AI Engineer"], "stages": ["HR"],
        "ans": "Companies invest heavily in training freshers on enterprise codebases, security protocols, and client domains during their first 6-12 months. Service agreements protect that investment from immediate turnover. Framework: 1) Confirm clearly that you are aware of the duration and terms, 2) Express complete comfort, 3) Reiterate that your career goal is to spend at least 2 to 3 years building solid foundations and delivering tangible business value in your first organization, so the agreement naturally aligns with your personal milestones. Illustrative example: 'Yes, I am completely aware of the service agreement terms and I am comfortable with it. The company invests substantial training and mentorship to onboard a fresher into production workflows. My objective is to stay with the company for at least 2 to 3 years to master the tech stack, see features through multiple production release cycles, and earn senior engineering trust, so the agreement fully aligns with my career plans.'",
        "kp": ["Direct, confident acceptance of the service agreement", "Understanding of company's training investment in freshers", "Clear commitment to 2-3 years of continuous growth and delivery"],
        "crit": ["Honest, professional alignment with corporate policies", "No evasive answers"],
        "cm": ["Arguing about the legality of employment bonds", "Acting surprised as if you had not researched the company's hiring terms"],
        "fu": ["What are your expectations from the company's fresher training program?", "How do you plan to measure your progress during your first year?"],
        "tags": ["master-bank", "hexaware", "company-workplace", "bond", "policy"]
    },
    {
        "q": "Are you comfortable switching from an AI Developer role to a Software Developer role?",
        "cat": "Company & Workplace", "sub": "Role Flexibility", "d": "Intermediate", "type": "hr",
        "roles": ["AI Engineer", "Software Development Engineer"], "stages": ["HR", "Technical Screening"],
        "ans": "Many candidates with AI degrees expect to only train deep neural networks all day, whereas enterprise demand often requires full-stack engineering, API pipelines, database management, and cloud infrastructure. Interviewers test whether you are dogmatic or adaptable. Strong answer: 1) Clarify that AI is fundamentally a component of modern software engineering; an AI model has zero business utility unless packaged inside robust, scalable software (APIs, databases, secure authentication, resilient frontends), 2) Express strong enthusiasm for general software development, 3) Highlight that mastering core software engineering (clean code, architecture, testing, CI/CD) will make you a far superior AI engineer in the long run. Illustrative example: 'Yes, I am completely comfortable. In fact, I believe that great AI systems are built on great software engineering foundations. A machine learning model is useless without reliable data pipelines, REST APIs, containerized deployment, and responsive user interfaces. Working as a software developer allows me to master production architecture, design patterns, and system scalability, which enhances my overall engineering value.'",
        "kp": ["Recognize that AI models must live inside production software systems", "Demonstrate genuine enthusiasm for broader software engineering (APIs, databases, architectures)", "Frame role flexibility as a holistic engineering career accelerator"],
        "crit": ["Adaptable, grounded engineering mindset over narrow theoretical dogma", "Understanding practical business deployment realities"],
        "cm": ["Saying 'No, I only want to work on deep learning models and nothing else'", "Looking disappointed or treating software development as inferior to AI"],
        "fu": ["What software engineering skills are most critical when deploying an AI model into production?", "Which programming languages do you prefer for general backend software development?"],
        "tags": ["master-bank", "ibm", "hexaware", "sws-ai", "company-workplace", "role-transition"]
    },
    {
        "q": "What is your opinion on climate change and how technology can help address it?",
        "cat": "Company & Workplace", "sub": "General Awareness & Tech Impact", "d": "Beginner", "type": "hr",
        "roles": ["Software Development Engineer", "AI Engineer"], "stages": ["HR"],
        "ans": "Interviewers use general awareness questions to assess how well-read, socially conscious, and articulate you are when connecting technology to global challenges. Framework: 1) Acknowledge the scientific urgency of climate change (rising temperatures, extreme weather, resource scarcity), 2) Highlight technological interventions: smart IoT sensors for water and air quality monitoring (like AquaAirX does), AI algorithms for renewable energy grid load balancing, predictive maintenance reducing industrial factory waste, and cloud data center energy efficiency, 3) Personal consciousness: sustainable commute and paperless digital workflows. Illustrative example: 'Climate change is one of the defining challenges of our generation. As engineers, our responsibility is to develop technologies that drive sustainability. For instance, IoT sensor networks allow real-time monitoring of emissions and water consumption, while machine learning optimizes solar and wind energy distribution grids by predicting demand fluctuations. Technology enables industries to transition from reactive pollution control to proactive resource efficiency.'",
        "kp": ["Balanced, scientifically grounded awareness of environmental challenges", "Connect technological capabilities (IoT, AI, predictive analytics) to sustainability solutions", "Professional, articulate delivery without extreme political bias"],
        "crit": ["Depth of general knowledge and structured articulation", "Ability to connect technology innovation to real-world impact"],
        "cm": ["Denying climate change or dismissing it as unimportant", "Rambling without connecting the topic to engineering or technology"],
        "fu": ["How can software engineers optimize code and cloud resources to reduce digital carbon footprints?", "Have you seen IoT applications in smart agriculture or water management?"],
        "tags": ["master-bank", "hexaware", "aquaairx", "general-opinion", "sustainability"]
    },

    # ---------------- PART 2: RESUME, PROJECTS & RESEARCH ----------------
    {
        "q": "Explain how your project connects to its database and how data flows through the application.",
        "cat": "Resume & Projects", "sub": "Database Connectivity & Flow", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Full-Stack Developer", "Backend Developer"], "stages": ["Technical"],
        "ans": "Interviewers assess database architecture and backend plumbing. Framework: 1) Connection establishment: Explain how your backend framework (FastAPI/Express/Spring) initializes database connections using an ORM (SQLAlchemy, Prisma, Hibernate) with connection pooling (e.g., connection pool size 10, max overflow 20) pointing to a database URL loaded securely from environment variables (`.env`). 2) Request handling: A client HTTP request arrives at an endpoint with payload data; Pydantic or schema validators parse and validate types. 3) Transaction session: The endpoint opens an asynchronous or scoped database session (`get_db` dependency), executes queries using ORM models or parameterized SQL queries, and commits the transaction (`db.commit()`). 4) Serialization & Response: Database records are serialized back to JSON response schemas and returned to the client with appropriate HTTP status codes. Errors trigger transaction rollbacks (`db.rollback()`) inside exception handlers.",
        "kp": ["Connection pooling manages reuse of database sockets under high concurrency", "Environment variables securely store database credentials", "Scoped sessions ensure clean transaction commit and rollback handling", "Validation schemas prevent SQL injection and invalid payloads"],
        "crit": ["Clarity on connection pooling, transaction boundaries, and serialization", "No confusion between client-side code and direct database connections"],
        "cm": ["Claiming the React frontend connects directly to the PostgreSQL database with passwords", "Leaving database sessions open without closing or committing"],
        "fu": ["Why is connection pooling essential in high-traffic web applications?", "How do you protect your queries against SQL injection attacks?"],
        "tags": ["master-bank", "aquaairx", "sws-ai", "wheelson", "database", "data-flow"]
    },
    {
        "q": "How would you secure your application against common vulnerabilities like SQL injection, XSS, and CSRF?",
        "cat": "Resume & Projects", "sub": "Application Security", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Full-Stack Developer", "Backend Developer"], "stages": ["Technical", "Final"],
        "ans": "Application security must be applied at every layer of the architecture: 1) SQL Injection: Never concatenate raw user input into SQL query strings. Use parameterized queries, prepared statements, or modern ORMs (SQLAlchemy, Hibernate) that automatically escape user input. 2) XSS (Cross-Site Scripting): Sanitize and escape all user-generated content before rendering it in the browser. Modern frameworks like React automatically escape JSX content. Implement Content Security Policy (CSP) headers to restrict script execution origins. 3) CSRF (Cross-Site Request Forgery): Use CSRF tokens on state-changing requests (POST/PUT/DELETE), or configure cookies with `SameSite=Strict` or `SameSite=Lax`. 4) Authentication & Secrets: Hash passwords using salted hashing algorithms (bcrypt/Argon2); store sensitive API keys in environment variables, never hardcoded in GitHub repositories; enforce HTTPS with TLS 1.3.",
        "kp": ["SQL Injection defense: Parameterized queries and ORM abstractions", "XSS defense: Output escaping (React auto-escaping) and Content Security Policy (CSP)", "CSRF defense: SameSite cookie flags and anti-CSRF tokens", "Password hashing: bcrypt/Argon2 with work factors"],
        "crit": ["Comprehensive defense-in-depth across database, browser, and network layers", "Accurate technical terminology without vague generalities"],
        "cm": ["Saying 'I use MD5 or SHA1 to hash user passwords' (both are cryptographically broken)", "Thinking HTTPS alone prevents SQL injection or XSS"],
        "fu": ["What is the difference between authorization and authentication?", "How does the principle of least privilege apply to database user permissions?"],
        "tags": ["master-bank", "ibm", "aquaairx", "sws-ai", "security", "web-security"]
    },
    {
        "q": "Explain your research work: what is the research problem, novelty, and evaluation methodology?",
        "cat": "Resume & Projects", "sub": "Academic Research & Publications", "d": "Advanced", "type": "technical",
        "roles": ["AI Engineer", "Machine Learning Engineer", "Data Scientist"], "stages": ["Technical"],
        "ans": "If you list a research project, paper, or patent on your resume, interviewers will examine your methodology deeply: 1) Problem Statement: Define the exact practical or theoretical limitation being addressed (e.g., low accuracy on low-light drone imagery, latency bottleneck in multi-document RAG retrieval). 2) Research Gap: What existing state-of-the-art methods (SOTA) failed to accomplish and why (e.g., standard CNNs lose contextual spatial detail; dense embeddings struggle with rare specialized domain keywords). 3) Proposed Novelty: Your specific algorithmic, architectural, or feature engineering innovation (e.g., hybrid sparse-dense retrieval with cross-encoder reranking, or introducing attention-guided residual feature fusion). 4) Empirical Evaluation: Dataset used, training/validation protocol, evaluation metrics (mAP, F1-score, BLEU, latency in ms), and statistical comparison demonstrating that your proposed approach outperformed existing baselines.",
        "kp": ["Clear structure: Problem -> Research Gap -> Proposed Method -> Empirical Validation", "Explicitly state what is novel about your contribution", "Quantify comparative performance against existing baseline algorithms"],
        "crit": ["Rigorous scientific explanation without claiming results you cannot defend", "Deep understanding of baseline limitations and evaluation metrics"],
        "cm": ["Claiming a standard library tutorial script as 'novel research'", "Inability to explain the mathematical formulation or evaluation metrics used in your paper"],
        "fu": ["What are the limitations of your proposed method, and what would you improve next?", "How does your model behave when tested on out-of-distribution real-world data?"],
        "tags": ["master-bank", "payoda", "sws-ai", "research", "machine-learning"]
    },

    # ---------------- PART 3: PROGRAMMING & CODING ----------------
    {
        "q": "Check whether two strings are anagrams of each other.",
        "cat": "Coding", "sub": "String Algorithms", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"], "stages": ["Technical Screening", "Technical"],
        "ans": "Two strings are anagrams if they contain the exact same characters with the exact same frequencies, regardless of order (e.g., 'listen' and 'silent'). Optimized Solution: Frequency Hash Map (Time: O(N), Space: O(K) where K is alphabet size). 1) If lengths differ, return False immediately. 2) Count frequencies using a hash map or array: increment for string A, decrement for string B. 3) If all counts equal zero, return True. Python Code:\n```python\nfrom collections import Counter\n\ndef is_anagram(s1: str, s2: str) -> bool:\n    # Clean and lowercase\n    clean1 = [c.lower() for c in s1 if c.isalnum()]\n    clean2 = [c.lower() for c in s2 if c.isalnum()]\n    if len(clean1) != len(clean2):\n        return False\n    return Counter(clean1) == Counter(clean2)\n\n# Or manual dictionary check (O(1) auxiliary space for 26 letters):\ndef is_anagram_manual(s1: str, s2: str) -> bool:\n    counts = {}\n    for c in s1.lower(): counts[c] = counts.get(c, 0) + 1\n    for c in s2.lower():\n        if c not in counts or counts[c] == 0: return False\n        counts[c] -= 1\n    return all(v == 0 for v in counts.values())\n```\nTime Complexity: O(N). Space Complexity: O(1) assuming a bounded alphabet (26 ASCII characters).",
        "kp": ["Check string lengths first as an O(1) early exit", "Hash map frequency counting runs in O(N) time and O(1) space for fixed alphabet", "Sorting approach (sorted(s1) == sorted(s2)) takes O(N log N) time"],
        "crit": ["Clean implementation handling case normalization and character frequencies", "Explaining trade-offs between O(N) hash map vs O(N log N) sorting"],
        "cm": ["Using sorting without mentioning that hash map counting is faster (O(N) vs O(N log N))", "Failing on strings with duplicate letters like 'aacc' vs 'ccac'"],
        "fu": ["How would you group an array of strings into anagram clusters (Group Anagrams)?", "What if the input contains millions of Unicode characters?"],
        "tags": ["master-bank", "ibm", "aquaairx", "coding", "strings", "anagrams"]
    },
    {
        "q": "Find the first non-repeating character in a string.",
        "cat": "Coding", "sub": "String Algorithms", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"], "stages": ["Technical Screening", "Technical"],
        "ans": "Problem: Given a string, find the first character that appears exactly once. Two-Pass Hash Map Approach (Time: O(N), Space: O(K) where K is unique characters <= 256): 1) Pass 1: Build a frequency dictionary counting occurrences of each character in the string. 2) Pass 2: Iterate through the string from left to right; the first character with count == 1 is the answer. 3) If no unique character exists, return None. Python Code:\n```python\ndef first_unique_char(s: str) -> str | None:\n    freq = {}\n    for c in s:\n        freq[c] = freq.get(c, 0) + 1\n    for c in s:\n        if freq[c] == 1:\n            return c\n    return None\n\n# Example: 'swiss' -> 'w', 'aabb' -> None\n```\nTime Complexity: O(N) (two sequential passes of length N). Space Complexity: O(1) because the character alphabet size is bounded (e.g. 26 lowercase English letters or 256 ASCII).",
        "kp": ["Two-pass algorithm: first pass counts frequency, second pass preserves original order", "Time complexity O(N); space complexity O(1) for bounded alphabet", "Avoids nested loops which would result in inefficient O(N^2) runtime"],
        "crit": ["Correct implementation maintaining original left-to-right ordering", "Explanation of time and space complexity"],
        "cm": ["Using s.count(c) inside a loop (results in O(N^2) time complexity)", "Iterating over the dictionary keys in languages where dictionary order is not preserved"],
        "fu": ["How would you solve this if characters arrive as a continuous, infinite data stream (Queue + Map)?", "What if the string length is 100GB and does not fit in RAM?"],
        "tags": ["master-bank", "ibm", "aquaairx", "coding", "strings", "hash-map"]
    },
    {
        "q": "Find the missing number in an array containing numbers from 1 to N.",
        "cat": "Coding", "sub": "Mathematical & Bitwise Algorithms", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"], "stages": ["Technical Screening", "Technical"],
        "ans": "Problem: Given an array of size N-1 containing distinct integers from 1 to N, find the missing integer. Two optimal approaches: 1) Mathematical Sum Formula: The sum of numbers from 1 to N is `N * (N + 1) // 2`. Subtract the sum of elements in the array from expected sum. The difference is the missing number. Time: O(N), Space: O(1). 2) XOR Bitwise Approach (Prevents Integer Overflow in languages with fixed integer sizes like C++/Java): XOR all numbers from 1 to N, and XOR with all array elements. Identical numbers cancel out (x ^ x = 0), leaving only the missing number. Python Code:\n```python\ndef find_missing_number_sum(arr: list[int]) -> int:\n    n = len(arr) + 1\n    expected_sum = n * (n + 1) // 2\n    return expected_sum - sum(arr)\n\ndef find_missing_number_xor(arr: list[int]) -> int:\n    n = len(arr) + 1\n    xor_all = 0\n    for i in range(1, n + 1):\n        xor_all ^= i\n    for num in arr:\n        xor_all ^= num\n    return xor_all\n```",
        "kp": ["Mathematical sum formula N*(N+1)//2 runs in O(N) time and O(1) space", "XOR bit manipulation avoids integer overflow in strongly-typed languages", "Demonstrates deep understanding of bitwise arithmetic"],
        "crit": ["Clean implementation of both mathematical and bitwise solutions", "Awareness of integer overflow risks on very large N in C/Java"],
        "cm": ["Sorting the array first (takes O(N log N) time unnecessarily)", "Using a hash set which consumes O(N) extra memory"],
        "fu": ["What if two numbers are missing from the array?", "How does the XOR method work when duplicate numbers exist?"],
        "tags": ["master-bank", "ibm", "aquaairx", "coding", "math", "bitwise"]
    },

    # ---------------- PART 5: JAVA & OOP ----------------
    {
        "q": "What is the difference between an abstract class and an interface in Java?",
        "cat": "Java & OOP", "sub": "Abstraction & Interfaces", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Java Developer"], "stages": ["Technical"],
        "ans": "Both abstract classes and interfaces achieve abstraction in Java, but serve fundamentally different architectural roles: 1) Multiple Inheritance: A class can implement MULTIPLE interfaces (`implements A, B, C`), but can extend only ONE class (`extends AbstractClass`). 2) State / Fields: An interface cannot maintain instance state; all variables declared in an interface are automatically `public static final` (constants). An abstract class can have instance variables, private fields, and constructors. 3) Method Implementations: An abstract class can have concrete methods, abstract methods, and protected/private helper methods. Since Java 8, interfaces can have `default` and `static` methods, and Java 9 added `private` methods, but interfaces primarily define a behavioral contract ('can-do'), whereas abstract classes define a shared identity hierarchy ('is-a'). 4) Constructors: Abstract classes have constructors (invoked via `super()` by subclasses); interfaces cannot have constructors.",
        "kp": ["Multiple inheritance: class can implement multiple interfaces, but extend only one class", "State: interfaces only have public static final constants; abstract classes can have mutable instance state", "Constructors: abstract classes have constructors; interfaces do not", "Use interface for contract decoupling ('can-do'); use abstract class for code reuse across related types ('is-a')"],
        "crit": ["Precise, up-to-date comparison including Java 8 default methods", "Architectural guidance on when to choose one over the other"],
        "cm": ["Stating that interfaces can NEVER have method implementations (Java 8 introduced default methods)", "Thinking you can instantiate an abstract class directly"],
        "fu": ["How does Java resolve diamond problem ambiguity with interface default methods?", "What is a functional interface and how does it enable Lambda expressions?"],
        "tags": ["master-bank", "ibm", "aquaairx", "java", "oop", "interfaces", "top-30"]
    },
    {
        "q": "What is the difference between checked and unchecked exceptions in Java?",
        "cat": "Java & OOP", "sub": "Exception Handling", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Java Developer"], "stages": ["Technical"],
        "ans": "Java's exception hierarchy derives from `java.lang.Throwable`: 1) Checked Exceptions: - Classes that inherit from `Exception` directly, EXCLUDING `RuntimeException`. - Checked at compile time: the compiler forces the developer to either handle the exception inside a `try-catch` block or declare it in the method signature using the `throws` keyword. - Represent recoverable external failures outside application control. Examples: `IOException`, `SQLException`, `ClassNotFoundException`. 2) Unchecked Exceptions (Runtime Exceptions): - Classes that inherit from `RuntimeException` or `Error`. - Not checked at compile time: the compiler does not require explicit handling or throws declarations. - Typically represent programming defects, logical bugs, or catastrophic system errors that should be fixed in code rather than caught. Examples: `NullPointerException`, `ArrayIndexOutOfBoundsException`, `ArithmeticException`, `OutOfMemoryError`.",
        "kp": ["Checked: subclass of Exception (not RuntimeException), verified at compile time (IOException, SQLException)", "Unchecked: subclass of RuntimeException, not checked at compile time (NullPointerException)", "Checked exceptions represent recoverable environmental conditions; unchecked represent logic bugs"],
        "crit": ["Accurate placement in the Throwable inheritance hierarchy", "Clear rationale for compiler enforcement on recoverable errors"],
        "cm": ["Confusing Error with Exception (Errors like OutOfMemoryError are fatal JVM conditions)", "Catching generic Throwable in application code"],
        "fu": ["What is try-with-resources in Java 7+ and how does AutoCloseable work?", "Why do modern frameworks like Spring prefer unchecked runtime exceptions?"],
        "tags": ["master-bank", "ibm", "aquaairx", "java", "exceptions"]
    },
    {
        "q": "What is the difference between final, finally, and finalize() in Java?",
        "cat": "Java & OOP", "sub": "Java Keywords & Lifecycle", "d": "Beginner", "type": "technical",
        "roles": ["Software Development Engineer", "Java Developer"], "stages": ["Technical Screening", "Technical"],
        "ans": "This is a classic Java terminology test: 1) `final` (Keyword / Access Modifier): - On a variable: makes it a constant (cannot be reassigned after initialization). - On a method: prevents method overriding by subclasses. - On a class: prevents inheritance (the class cannot be subclassed, e.g., `final class String`). 2) `finally` (Exception Handling Block): - A block paired with `try-catch` that is guaranteed to execute regardless of whether an exception is thrown or caught. - Used for critical resource cleanup: closing database connections, file handles, or network sockets. (Executes even if a `return` statement is encountered inside `try`, failing only if `System.exit(0)` is called or JVM crashes). 3) `finalize()` (Deprecated Object Method): - A protected method on `java.lang.Object` invoked by the Garbage Collector before reclaiming an unreachable object's memory. - Deprecated since Java 9 because it is unpredictable, dangerous, and causes memory leaks. Replaced by `try-with-resources` and `java.lang.ref.Cleaner`.",
        "kp": ["final: modifier for constants, non-overridable methods, and non-inheritable classes", "finally: cleanup block in try-catch guaranteed to execute", "finalize(): deprecated Object method historically called by garbage collector"],
        "crit": ["Clear, crisp distinction across keyword modifier, code block, and deprecated method", "Understanding why finalize() was deprecated in modern Java"],
        "cm": ["Confusing Python's finally block with Java's finalize() method", "Believing finalize() is guaranteed to execute immediately when an object goes out of scope"],
        "fu": ["Does a finally block execute if you call return in the try block?", "What is the only scenario where a finally block will NOT execute?"],
        "tags": ["master-bank", "ibm", "aquaairx", "java", "keywords", "top-30"]
    },

    # ---------------- PART 6: SQL & DATABASES ----------------
    {
        "q": "What is the difference between WHERE and HAVING clauses in SQL?",
        "cat": "SQL & Analytics", "sub": "Filtering Clauses", "d": "Beginner", "type": "technical",
        "roles": ["Data Analyst", "Software Development Engineer", "Backend Developer"], "stages": ["Technical Screening", "Technical"],
        "ans": "Both clauses filter records in SQL, but at fundamentally different stages of query execution: 1) `WHERE` Clause: - Filters individual rows BEFORE any grouping (`GROUP BY`) or aggregations occur. - Cannot contain aggregate functions (e.g., `WHERE SUM(salary) > 50000` is illegal and causes a syntax error). - Operates directly on table columns and can utilize database indexes for performance. 2) `HAVING` Clause: - Filters summarized groups AFTER `GROUP BY` aggregation has computed group totals. - Specifically designed to filter on aggregate functions (e.g., `HAVING COUNT(*) > 5` or `HAVING AVG(salary) >= 75000`). - Executes later in the SQL logical query processing order. Example Query:\n```sql\nSELECT department_id, AVG(salary) as avg_sal\nFROM Employee\nWHERE status = 'Active'         -- Filters raw rows before grouping\nGROUP BY department_id\nHAVING AVG(salary) > 60000;      -- Filters aggregated department groups\n```",
        "kp": ["WHERE filters rows BEFORE grouping; cannot use aggregate functions", "HAVING filters groups AFTER aggregation; specifically used with SUM, AVG, COUNT", "WHERE is more performant because it prunes rows before expensive group computations"],
        "crit": ["Clear explanation of query execution order: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT", "Correct usage in example aggregation query"],
        "cm": ["Putting aggregate conditions in the WHERE clause", "Using HAVING for row-level filters that could have been handled more efficiently in WHERE"],
        "fu": ["What is the complete logical execution order of a SQL SELECT statement?", "Can you use HAVING without a GROUP BY clause in SQL?"],
        "tags": ["master-bank", "ibm", "sws-ai", "sql", "filtering", "top-30"]
    },
    {
        "q": "What is the difference between DELETE, TRUNCATE, and DROP in SQL?",
        "cat": "SQL & Analytics", "sub": "DDL vs DML Commands", "d": "Beginner", "type": "technical",
        "roles": ["Data Analyst", "Software Development Engineer", "Backend Developer"], "stages": ["Technical Screening", "Technical"],
        "ans": "1) `DELETE` (DML - Data Manipulation Language): - Deletes specific rows matching a `WHERE` condition (or all rows if WHERE is omitted). - Row-by-row operation: logs each deleted row in the transaction log, making it slower on massive tables. - Can be rolled back inside a transaction. - Does NOT reset auto-increment identity counters. - Table structure and schema remain intact. 2) `TRUNCATE` (DDL - Data Definition Language): - Removes ALL rows from a table by deallocating data pages. - Cannot have a `WHERE` clause. - Much faster than DELETE because it logs page deallocations rather than individual row deletions. - Resets auto-increment identity counters back to seed value. - Table structure remains intact. Cannot be run on tables referenced by active Foreign Key constraints. 3) `DROP` (DDL - Data Definition Language): - Completely deletes the table structure, data, indexes, permissions, and constraints from the database catalog. - The table ceases to exist entirely. Cannot be rolled back in many relational systems without external backups.",
        "kp": ["DELETE: DML, row-by-row, supports WHERE, can be rolled back, keeps identity counter", "TRUNCATE: DDL, deallocates pages, removes all rows rapidly, resets identity counter, keeps table structure", "DROP: DDL, destroys data and table schema permanently"],
        "crit": ["Systematic comparison across DDL/DML classification, speed, rollback capability, and schema retention", "Understanding foreign key restrictions on TRUNCATE"],
        "cm": ["Believing TRUNCATE can take a WHERE clause", "Thinking TRUNCATE deletes the table schema"],
        "fu": ["Why does TRUNCATE fail if another table has a foreign key referencing the target table?", "Can TRUNCATE be rolled back inside a transaction in PostgreSQL?"],
        "tags": ["master-bank", "ibm", "sws-ai", "sql", "ddl-dml", "top-30"]
    },
    {
        "q": "What are the ACID properties in database transactions?",
        "cat": "SQL & Analytics", "sub": "Database Transactions", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Data Analyst"], "stages": ["Technical", "Final"],
        "ans": "ACID properties guarantee that database transactions are processed reliably, preserving data integrity in multi-user concurrent systems: 1) Atomicity ('All or Nothing'): A transaction is treated as a single indivisible unit. Either all operations succeed and commit, or if any part fails, the entire transaction rolls back completely to its initial state. Real-world example: A bank transfer deducting $100 from Account A and adding $100 to Account B. If the system crashes after deducting, Atomicity ensures Account A is refunded. 2) Consistency: A transaction transitions the database from one valid state to another, strictly satisfying all defined schema constraints, triggers, primary keys, foreign keys, and cascade rules. 3) Isolation: Concurrently executing transactions cannot interfere with or see each other's intermediate, uncommitted states. Controlled via SQL isolation levels (Read Uncommitted, Read Committed, Repeatable Read, Serializable) using locks or Multi-Version Concurrency Control (MVCC). 4) Durability: Once a transaction commits, its changes are permanently recorded in non-volatile storage (WAL / Write-Ahead Logging) and will survive system crashes or power outages.",
        "kp": ["Atomicity: all operations succeed or all roll back (all-or-nothing)", "Consistency: database transitions strictly between valid constraint-compliant states", "Isolation: concurrent transactions execute without cross-contamination (MVCC / locking)", "Durability: committed data survives power failures and crashes via WAL"],
        "crit": ["Clear, accurate definition of all four properties with practical banking or eCommerce examples", "Understanding concurrency control and crash recovery mechanisms"],
        "cm": ["Confusing Consistency in ACID with Consistency in CAP theorem", "Vague answers without concrete database examples"],
        "fu": ["What are dirty reads, non-repeatable reads, and phantom reads?", "How does Write-Ahead Logging (WAL) guarantee durability?"],
        "tags": ["master-bank", "ibm", "sws-ai", "sql", "acid", "transactions", "top-30"]
    },
    {
        "q": "Write a query to insert all records from Table A into Table B.",
        "cat": "SQL & Analytics", "sub": "Data Manipulation Queries", "d": "Beginner", "type": "technical",
        "roles": ["Data Analyst", "Software Development Engineer", "Backend Developer"], "stages": ["Technical Screening", "Technical"],
        "ans": "To copy data from one existing table into another existing table with compatible column schemas, use the `INSERT INTO ... SELECT` statement: Syntax & Example:\n```sql\nINSERT INTO TableB (id, name, department, salary)\nSELECT id, name, department, salary\nFROM TableA;\n```\nKey Rules: 1) Column alignment: The number of columns in the SELECT clause must match the target INSERT columns in quantity and compatible data types. 2) Existing table: Table B must already exist in the database. 3) Constraints: If Table B has Primary Key or Unique constraints, inserting duplicate keys from Table A will trigger constraint violation errors. In PostgreSQL/SQLite, you can use `ON CONFLICT (id) DO NOTHING` or `DO UPDATE` to handle collisions gracefully. Alternative for creating a brand-new table: `CREATE TABLE TableB AS SELECT * FROM TableA;`.",
        "kp": ["INSERT INTO TableB (...) SELECT ... FROM TableA copies records between existing tables", "Columns must match in number, order, and compatible data types", "Handle potential Primary Key constraint violations with ON CONFLICT / MERGE"],
        "crit": ["Syntactically valid SQL statement with column mapping", "Awareness of primary key conflicts and schema requirements"],
        "cm": ["Using VALUES keyword alongside SELECT (e.g. INSERT INTO ... VALUES (SELECT ...)) which is invalid SQL syntax", "Assuming Table B is created automatically by INSERT INTO"],
        "fu": ["How do you update existing rows and insert new ones in a single query (UPSERT / MERGE)?", "What is the difference between INSERT INTO ... SELECT and SELECT ... INTO in SQL Server?"],
        "tags": ["master-bank", "ibm", "sws-ai", "sql", "queries", "insert-into"]
    },

    # ---------------- PART 9: AI, ML, GENAI & RAG ----------------
    {
        "q": "What is the bias-variance trade-off in machine learning?",
        "cat": "ML, AI & GenAI", "sub": "Statistical Learning Theory", "d": "Intermediate", "type": "technical",
        "roles": ["Machine Learning Engineer", "AI Engineer", "Data Scientist"], "stages": ["Technical"],
        "ans": "The bias-variance trade-off is the central challenge in supervised machine learning for achieving generalization on unseen data: 1) Bias (Error due to overly simplistic assumptions): - Occurs when a model makes strong, rigid assumptions that miss underlying data patterns. - Leads to Underfitting: High training error and high test error. - Example: Fitting a simple linear regression line to complex, non-linear parabolic data. 2) Variance (Error due to excessive model sensitivity to training noise): - Occurs when a model is overly complex, capturing random fluctuations and noise in the training set rather than the underlying pattern. - Leads to Overfitting: Extremely low training error, but high validation/test error. - Example: An unconstrained decision tree with depth 50 that memorizes every outlier. 3) The Trade-off: Total Error = Bias^2 + Variance + Irreducible Noise. As model complexity increases, bias decreases but variance increases. The goal of machine learning engineering is to find the sweet spot of model complexity (via regularization, pruning, cross-validation) that minimizes total prediction error on unseen data.",
        "kp": ["High Bias = Underfitting (overly simplistic model, high train & test error)", "High Variance = Overfitting (overly complex model, low train error, high test error)", "Total Error = Bias^2 + Variance + Irreducible Error", "Optimal model complexity balances bias and variance to minimize generalization error"],
        "crit": ["Clear, accurate mathematical and conceptual explanation", "Concrete techniques to diagnose and balance bias and variance"],
        "cm": ["Confusing bias in statistics with societal/human bias in AI ethics", "Believing you can reduce both bias and variance to zero simultaneously"],
        "fu": ["Does bagging reduce bias or variance? Does boosting reduce bias or variance?", "How does K-fold cross-validation help diagnose high bias versus high variance?"],
        "tags": ["master-bank", "payoda", "sws-ai", "ibm", "machine-learning", "bias-variance", "top-30"]
    },
    {
        "q": "How does a Retrieval-Augmented Generation (RAG) pipeline work, and what are its main components?",
        "cat": "ML, AI & GenAI", "sub": "Generative AI & RAG", "d": "Intermediate", "type": "technical",
        "roles": ["AI Engineer", "Generative AI Engineer", "Full-Stack Developer"], "stages": ["Technical", "Final"],
        "ans": "A RAG pipeline connects external factual enterprise knowledge to a Large Language Model without retraining its weights. 1) Ingestion & Indexing Phase: - Document Extraction: Parsing raw PDF documents, markdown, or databases into clean text. - Chunking: Splitting text into manageable chunks (e.g., 500-1000 tokens with 10% overlap) to maintain semantic context within vector embedding limits. - Vector Embedding: Converting each text chunk into a high-dimensional vector using an embedding model (e.g., OpenAI text-embedding-3-small, BGE). - Vector Store: Indexing vector embeddings and chunk metadata into a vector database (Pinecone, Milvus, pgvector). 2) Query & Retrieval Phase: - The user submits a question; the question is converted into an embedding using the same embedding model. - Similarity Search: Computing cosine similarity or approximate nearest neighbors (HNSW index) to retrieve the top-K most relevant chunks. - Optional Reranking: A cross-encoder reranker scores the top chunks for relevance precision. 3) Generation Phase: - Prompt Augmentation: The retrieved chunks are injected into the system prompt as context alongside user query: 'Answer the question strictly using the provided context...'. - LLM Synthesis: The LLM generates a grounded, accurate response with exact source citations, eliminating hallucinations.",
        "kp": ["Three core phases: Document Ingestion/Chunking -> Semantic Vector Search -> Grounded LLM Generation", "Embedding models map semantic meaning to high-dimensional vector spaces", "Similarity search (Cosine / HNSW) finds closest contextual chunks", "Eliminates hallucinations and keeps knowledge current without model fine-tuning"],
        "crit": ["Complete, end-to-end architectural explanation of ingestion, retrieval, and generation", "Understanding chunking trade-offs, vector similarity, and context injection"],
        "cm": ["Assuming RAG fine-tunes or modifies the LLM's weights", "Ignoring chunk overlap, which leads to split sentences and lost semantic context"],
        "fu": ["What is the difference between dense retrieval (vector embeddings) and sparse retrieval (BM25)?", "How do you handle tables and diagrams in multimodal RAG pipelines?"],
        "tags": ["master-bank", "sws-ai", "payoda", "rag", "genai", "embeddings", "vector-db", "top-30"]
    },
    {
        "q": "What is temperature in a Large Language Model, and how does it affect generated output?",
        "cat": "ML, AI & GenAI", "sub": "LLM Inference Parameters", "d": "Beginner", "type": "technical",
        "roles": ["AI Engineer", "Generative AI Engineer", "Software Development Engineer"], "stages": ["Technical"],
        "ans": "Temperature is a hyperparameter that controls the randomness and creativity of an LLM's token generation by scaling the logits (unnormalized log-probabilities) before applying the softmax function: `P(token_i) = exp(logit_i / T) / sum(exp(logit_j / T))`. 1) Low Temperature (T -> 0, e.g., 0.0 to 0.2): - Sharpens the probability distribution, heavily favoring the highest-probability token. - Output is highly deterministic, factual, concise, and repeatable. - Best for: Code generation, SQL query synthesis, classification, math calculations, and strict JSON extraction where hallucination or variation is undesirable. 2) Moderate Temperature (T = 0.7): - Balanced distribution; introduces moderate vocabulary diversity while preserving coherence. - Best for: General chatbots, document summarization, drafting emails. 3) High Temperature (T -> 1.0 to 1.5): - Flattens the probability distribution, giving lower-probability words a higher chance of selection. - Output is highly diverse, creative, and novel, but increases the risk of rambling, incoherence, and hallucinations. - Best for: Brainstorming marketing hooks, creative storytelling, poetry.",
        "kp": ["Temperature scales logits in the softmax probability distribution", "Low temperature (0.0 - 0.2): deterministic, factual, ideal for code, SQL, and JSON", "High temperature (0.8 - 1.2): creative, diverse, higher hallucination risk", "Temperature = 0 approaches greedy decoding (always picking argmax token)"],
        "crit": ["Accurate mathematical explanation of logit scaling before softmax", "Clear operational guidelines for choosing temperatures across real-world software tasks"],
        "cm": ["Thinking temperature changes the model's underlying weights", "Using high temperature (0.9) for structured JSON data extraction"],
        "fu": ["What is Top-P (nucleus sampling) and how does it interact with temperature?", "What is Top-K sampling?"],
        "tags": ["master-bank", "sws-ai", "genai", "llm", "temperature", "prompt-engineering"]
    },

    # ---------------- PART 10: NETWORKING & SECURITY ----------------
    {
        "q": "What is the difference between symmetric and asymmetric encryption?",
        "cat": "Networking & IoT", "sub": "Cryptography & Security", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer"], "stages": ["Technical"],
        "ans": "Cryptography secures data transmission using mathematical algorithms classified by key usage: 1) Symmetric Encryption (Secret Key): - Uses a SINGLE shared secret key for both encryption and decryption. Both sender and receiver must possess this secret key. - Performance: Extremely fast and computationally lightweight; ideal for encrypting large volumes of data (bulk file encryption, database disk encryption). - Challenge: Secure Key Distribution—how to safely share the secret key over an untrusted network without it being intercepted. - Common Algorithms: AES (Advanced Encryption Standard - AES-128, AES-256), ChaCha20, DES. 2) Asymmetric Encryption (Public-Key Cryptography): - Uses a MATHEMATICALLY LINKED KEY PAIR: a Public Key (freely distributed to anyone to encrypt data) and a Private Key (kept secret by the receiver to decrypt data). - Performance: Computationally expensive, much slower than symmetric encryption (up to 1,000x slower due to large prime number factorization or elliptic curve math). - Solves Key Exchange: Anyone can encrypt a message using your public key, but only you can decrypt it using your private key. - Common Algorithms: RSA, ECC (Elliptic Curve Cryptography), Diffie-Hellman. 3) Modern Hybrid Encryption (SSL/TLS): HTTPS uses asymmetric encryption (RSA/ECC) during the initial TLS handshake to securely negotiate a temporary symmetric session key, and then switches to symmetric encryption (AES) for all subsequent application data transfer.",
        "kp": ["Symmetric: single secret key for both encryption and decryption (fast, bulk data, AES)", "Asymmetric: public key encrypts, private key decrypts (slower, solves key exchange, RSA/ECC)", "HTTPS uses hybrid approach: asymmetric handshake negotiates fast symmetric session key"],
        "crit": ["Clear, accurate comparison across speed, key management, and algorithms", "Understanding the hybrid TLS handshake combining both systems"],
        "cm": ["Believing public keys can decrypt messages encrypted with the same public key", "Thinking asymmetric encryption is fast enough for streaming bulk video files"],
        "fu": ["How do digital signatures work using the sender's private key and receiver's public key?", "What is forward secrecy in TLS 1.3?"] ,
        "tags": ["master-bank", "ibm", "security", "encryption", "networking"]
    },
    {
        "q": "What is the difference between HTTP and HTTPS, and how does the SSL/TLS handshake work?",
        "cat": "Networking & IoT", "sub": "Web Protocols & Security", "d": "Beginner", "type": "technical",
        "roles": ["Software Development Engineer", "Full-Stack Developer", "Backend Developer"], "stages": ["Technical Screening", "Technical"],
        "ans": "1) HTTP (Hypertext Transfer Protocol): Operates over port 80; transmits data in plaintext. Any attacker on the local network (Wi-Fi eavesdropping, ISP inspection) can read and modify packets (passwords, credit card numbers, session cookies) via Man-In-The-Middle (MITM) attacks. 2) HTTPS (HTTP Secure): Operates over port 443; layers standard HTTP over an encrypted SSL/TLS tunnel, providing three vital protections: - Encryption: Data cannot be intercepted in transit. - Data Integrity: Data cannot be tampered with or modified in transit without detection. - Authentication: Digital certificates verify that the client is communicating with the legitimate server rather than an impostor. 3) TLS Handshake (High-Level): - Client Hello: Browser sends supported TLS versions and cryptographic cipher suites. - Server Hello & Certificate: Server responds with chosen cipher suite and its digital certificate signed by a trusted Certificate Authority (CA). - Verification & Key Exchange: Browser verifies certificate against trusted root CAs, and both parties negotiate a shared symmetric session key using asymmetric cryptography (Diffie-Hellman / RSA). - Finished: Both switch to encrypted communication using the symmetric session key.",
        "kp": ["HTTP is plaintext on port 80; HTTPS is encrypted via TLS on port 443", "HTTPS guarantees: Confidentiality (encryption), Integrity (HMAC), and Server Authentication (CA certificate)", "TLS handshake establishes secure symmetric session key before transmitting HTTP payload"],
        "crit": ["Accurate explanation of the 3 core security pillars of HTTPS", "Understanding certificate authorities and session key negotiation"],
        "cm": ["Saying HTTPS makes application source code immune to SQL injection or XSS", "Thinking SSL and TLS are two completely different companies"],
        "fu": ["What happens in the browser when an SSL certificate is expired or self-signed?", "What is HSTS (HTTP Strict Transport Security)?"],
        "tags": ["master-bank", "ibm", "aquaairx", "wheelson", "networking", "https", "ssl-tls", "top-30"]
    }
]


def run():
    with SessionLocal() as db:
        existing_rows = db.scalars(select(Question)).all()
        hash_to_question = {row.question_hash: row for row in existing_rows}
        id_to_question = {row.id: row for row in existing_rows}

        created = 0
        updated = 0

        for item in QUESTIONS:
            q_text = item["q"]
            h = question_fingerprint(q_text)
            tags = list(item.get("tags", []))

            if h in hash_to_question:
                row = hash_to_question[h]
                merged_tags = list(dict.fromkeys(list(row.tags or []) + tags))
                row.tags = merged_tags
                updated += 1
                log.info(f"Updated tags on: {row.id} - {row.question[:40]}")
            else:
                cat_slug = item["cat"].lower().replace("&", "").replace(",", "").replace(" ", "-")[:4]
                sub_count = sum(1 for qid in id_to_question if qid.startswith(f"mst-{cat_slug}"))
                new_id = f"mst-{cat_slug}-{sub_count + 1:03d}"

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
                log.info(f"Created: {new_id} - {q_text[:40]}")

        db.commit()
        print(f"Full Master Bank Seeding Completed: Created {created}, Updated {updated}.")


if __name__ == "__main__":
    run()
