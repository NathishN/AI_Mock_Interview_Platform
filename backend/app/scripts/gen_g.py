"""Generator for Category G: Company, Workplace, and Final-Round Questions (50 questions).
25 questions in 01.json, 25 in 02.json.
Must include 'illustrative' marker in every reference answer.
"""
import json
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parents[2] / "data" / "src" / "G_company"

PART1 = [
    {
        "q": "What do you know about our company's core products, revenue model, and primary competitors?",
        "sub": "Company Research",
        "d": "Beginner",
        "ans": "Interviewer is assessing: genuine interest, preparation rigor, and business literacy. Never recite generic taglines from the homepage. State their primary product offerings, who their paying customers are (B2B, B2C, enterprise), how they monetize (SaaS subscriptions, transaction fees, consulting services), and name two or three verifiable competitors. Illustrative example (replace with verified company facts): 'I researched [Company] and know you specialize in [Product/Service], primarily serving [Customer Segment]. Your business model revolves around [Monetization Strategy], and key market competitors include [Competitor 1] and [Competitor 2]. I was particularly impressed by your recent launch of [Recent Product/Feature].'",
        "kp": ["Specific core products and target customer segments", "Understanding of monetization/business model", "Knowledge of competitive market landscape", "Recent company announcements, tech blogs, or milestones"],
        "cm": ["Saying 'You are a very big multinational company with great culture' without mentioning any product", "Confusing B2B enterprise offerings with consumer apps", "Guessing competitors or business model without checking official sources"],
        "fu": ["What recent news or engineering blog post from our company caught your attention?", "If you were advising our leadership, which competitor threat would you monitor most closely?"],
        "tags": ["company-research", "business-model", "competitors", "fresher"]
    },
    {
        "q": "What would be your concrete 30-60-90 day plan if hired as a fresher into this role?",
        "sub": "Onboarding & Ramp-up",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: self-drive, structured planning, and proactive ownership. Divide your response into three milestones: Days 1-30 (Listen and Learn: master codebase, set up environments, understand team conventions, ship first small bug fix), Days 31-60 (Contribute: take ownership of independent user stories, reduce reliance on senior mentors, participate actively in code reviews), and Days 61-90 (Deliver & Optimize: contribute to feature architecture, identify documentation gaps, propose minor optimizations). Illustrative example (replace with your role details): 'In the first 30 days, my goal is to absorb team conventions, set up local environments without friction, and fix my first two backlog bugs. By day 60, I want to take ownership of mid-sized tickets independently. By day 90, I plan to contribute to production feature releases and document setup hurdles to help the next onboarding junior.'",
        "kp": ["Structured 30-60-90 day milestone roadmap", "First 30 days: onboarding, codebase familiarity, small fixes", "60 days: independent task execution, active PR contributions", "90 days: feature ownership, documentation, and minor optimizations"],
        "cm": ["Promising to 'revolutionize company architecture' in your first 30 days (unrealistic arrogance)", "Having no plan and saying 'I will just do whatever my manager tells me'", "Ignoring the learning and listening phase required for new codebases"],
        "fu": ["How would you measure whether your first 30 days were successful?", "What would you do if your assigned mentor was too busy to answer onboarding questions?"],
        "tags": ["30-60-90-plan", "onboarding", "ramp-up", "initiative"]
    },
    {
        "q": "What would you do if you were assigned a task using a technology or framework you have never used before?",
        "sub": "Learning Agility",
        "d": "Beginner",
        "ans": "Interviewer is assessing: learning agility, adaptability, and resourcefulness under uncertainty. Describe a systematic 4-step ramp-up strategy: 1) Understand requirements and output expectations from the lead, 2) Study official documentation, quickstart guides, and architectural design patterns, 3) Build a small throwaway proof-of-concept (POC) to test core mechanics and edge cases, and 4) Implement the production code following team conventions while asking targeted questions. Illustrative example (replace with your experience): 'When assigned [New Tech] during my college project, I didn't panic. I spent the first morning studying official docs and building a minimal POC. Once I understood the data flow, I mapped concepts back to [Familiar Tech], implemented the feature, and asked my senior for review on my architectural choices.'",
        "kp": ["Methodical ramp-up: official docs -> minimal proof-of-concept -> production code", "Map unfamiliar concepts to familiar foundational principles", "Timeboxed independent exploration before asking senior mentors", "Growth mindset embracing technology changes"],
        "cm": ["Saying 'I only work with technologies I learned in college'", "Asking senior developers for help immediately before reading documentation", "Copy-pasting unverified code snippets from AI or Stack Overflow without understanding"],
        "fu": ["How do you decide between reading official documentation vs following a video tutorial?", "How much time do you spend stuck before reaching out to a teammate?"],
        "tags": ["learning-agility", "adaptability", "problem-solving", "fresher"]
    },
    {
        "q": "What would you do if you strongly disagreed with a technical decision made by your manager or team lead?",
        "sub": "Conflict & Hierarchy",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: professional communication, respect for hierarchy, and the principle of 'Disagree and Commit'. Explain that you would: 1) First seek to understand their rationale and constraints (business deadlines, technical debt, legacy dependencies), 2) Request a private 1-on-1 meeting to present your technical counter-argument with objective data, benchmarks, or trade-off comparisons rather than emotional opinions, and 3) If the manager evaluates the data and still decides on their original approach, commit fully to their decision ('Disagree and Commit') and execute it with 100% effort without passive-aggressive resistance. Illustrative example (replace with your facts): 'In my team project, our lead chose [Approach A] while I preferred [Approach B]. I scheduled a short discussion, showed latency benchmarks comparing both, but when he explained that [Approach A] was required for deadline constraints, I accepted his decision and focused completely on making [Approach A] work flawlessly.'",
        "kp": ["Seek to understand manager rationale and hidden constraints first", "Present technical counter-arguments privately with objective benchmarks/data", "Avoid emotional or public confrontations in front of the team", "Practice 'Disagree and Commit': support the final decision fully once made"],
        "cm": ["Saying 'I would just do what they said silently without questioning' (no backbone)", "Saying 'I would go over their head to the director' (unprofessional escalation)", "Subverting the manager's decision by implementing your own way secretly"],
        "fu": ["What would you do if you believed the manager's decision violated legal, ethical, or security policies?", "What does 'Disagree and Commit' mean for team velocity?"],
        "tags": ["workplace-conflict", "disagree-and-commit", "hierarchy", "communication"]
    },
    {
        "q": "Tell me about a time you accidentally broke something or made a serious mistake. How did you handle it?",
        "sub": "Mistake Recovery",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: accountability, honesty, emotional composure, and root-cause prevention. Use a 4-part structure: 1) Immediate containment (reverting changes, alerting affected parties), 2) Transparent communication without blame-shifting, 3) Implementing a permanent root-cause fix, and 4) Institutionalizing a preventive check (test, linter, checklist) so the mistake can never recur. Illustrative example (replace with your real experience): 'While deploying a project demo, I accidentally overwrote our database schema migration script, causing endpoint 500 errors. I immediately notified the team, reverted to the previous commit, and restored the database from our latest backup. After restoring service, I added automated schema migration validation to our pre-commit hook so accidental overrides are caught before committing.'",
        "kp": ["Immediate transparency: notify team and contain the issue first", "No excuse-making or blaming tools/teammates", "Root-cause analysis to understand why it failed", "Preventive automated safeguard instituted to prevent regression"],
        "cm": ["Claiming 'I have never made a mistake in my life'", "Hiding the mistake hoping nobody notices", "Blaming someone else for the failure"],
        "fu": ["How did your relationship with your team change after you owned that mistake?", "What is a blameless post-mortem in engineering culture?"],
        "tags": ["mistakes", "accountability", "blameless-postmortem", "resilience"]
    },
    {
        "q": "What would you do if your project deadline was cut in half or became completely unrealistic?",
        "sub": "Deadline Management",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: realistic prioritization, scope management, and proactive communication under pressure. Explain that software deadlines cannot be met by simply 'working 24 hours a day', as that introduces catastrophic bugs. Instead: 1) Audit the backlog and categorize features into Must-Have (MVP core), Should-Have, and Nice-to-Have, 2) Propose scoping down to the MVP so a stable, tested core is delivered on the new date, 3) Communicate the trade-off transparently to the manager early, and 4) Schedule remaining secondary features for a follow-up release. Illustrative example (replace with your real facts): 'When our college project submission was moved forward by two weeks, our team held an emergency triage. We agreed to cut the recommendation engine and focus strictly on delivering a rock-solid core CRUD workflow. By communicating this scope reduction to our evaluator early, we delivered a bug-free system on time rather than a broken complete feature set.'",
        "kp": ["Triage features: isolate core MVP from optional enhancements", "Negotiate scope down rather than cutting testing or quality", "Proactive, early communication with management about trade-offs", "Deliver a stable smaller release rather than a broken large release"],
        "cm": ["Promising to work 20 hours a day without sleep (leads to burnout and buggy code)", "Silently missing the deadline without warning stakeholders until the final day", "Cutting out all testing and validation to rush features out the door"],
        "fu": ["How do you tell a manager that a deadline is impossible without sounding negative?", "What is the Iron Triangle of project management (Scope, Time, Cost/Quality)?"],
        "tags": ["deadlines", "prioritization", "scope-management", "communication"]
    },
    {
        "q": "How would you handle an unhappy client or angry business stakeholder who is criticizing your team's software?",
        "sub": "Stakeholder Management",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: emotional intelligence, active listening, and de-escalation skills. Follow the HEAR principle: 1) Hear: listen patiently without interrupting, allowing them to fully vent their frustration, 2) Empathize: acknowledge the impact on their business ('I understand this downtime caused missed customer orders, and that is unacceptable'), 3) Analyze: ask clarifying questions to isolate the exact technical issue, and 4) Resolve: propose an immediate short-term mitigation followed by a clear timeline for the permanent fix, keeping them updated proactively. Illustrative example (replace with your experience): 'When an external judge critiqued our slow UI during a project review, I didn't become defensive. I acknowledged the latency issue, explained our profiling findings, and walked them through how our upcoming Redis caching layer addressed it, turning their criticism into a constructive discussion.'",
        "kp": ["Active listening without defensive interruptions", "Empathetic acknowledgment of the real business impact", "Fact-based analysis of the root technical issue", "Clear communication of immediate mitigations and long-term fix timeline"],
        "cm": ["Becoming defensive or arguing back with the client", "Blaming the user for 'using the application wrong'", "Promising instant fixes before understanding the technical root cause"],
        "fu": ["How do you balance client feature demands against backend technical debt?", "What do you do if a client demands a feature that violates engineering best practices?"],
        "tags": ["stakeholder-management", "empathy", "de-escalation", "client-communication"]
    },
    {
        "q": "How do you decide between shipping code quickly to meet business needs versus spending time refactoring for clean architecture?",
        "sub": "Engineering Pragmatism",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: engineering pragmatism and technical debt awareness. Software engineering is a balance between business speed and long-term maintainability. Explain using the concept of intentional vs accidental technical debt: in early-stage validation or high-priority market releases, taking on measured technical debt to ship an MVP fast is justified. However, technical debt must be paid down iteratively. If code is in the core business critical path where future features build upon it, high architecture rigor and test coverage are non-negotiable. Illustrative example (replace with your experience): 'For our initial project demo, I used simple SQLite queries to validate the user flow fast. Once the concept was validated, I refactored the data layer to PostgreSQL with proper indexing and connection pooling before testing under load, ensuring business speed didn't compromise long-term scalability.'",
        "kp": ["Awareness of intentional technical debt as a business trade-off", "Distinguish core critical paths (require high clean code) from throwaway experiments", "Pragmatism: perfect code that misses the market window is useless", "Commitment to scheduling refactoring sprints to pay down debt"],
        "cm": ["Dogmatically refusing to ship code until it is '100% architecturally perfect'", "Writing sloppy, unmaintainable spaghetti code and calling it 'agile'", "Never paying down technical debt until the entire system collapses"],
        "fu": ["What is technical debt and how do you track it in a team's backlog?", "When does refactoring become premature optimization?"],
        "tags": ["technical-debt", "pragmatism", "refactoring", "software-engineering"]
    },
    {
        "q": "What if you were assigned to a project or domain you find uninteresting, or asked to do software testing / production support?",
        "sub": "Professional Adaptability",
        "d": "Beginner",
        "ans": "Interviewer is assessing: humility, team-first attitude, and professional maturity. Freshers often expect only cutting-edge AI development, while businesses require support, testing, and legacy maintenance. Explain that every assignment provides valuable engineering lessons: production support teaches debugging under pressure, system observability, and real customer pain points; QA teaches testing rigor and edge-case thinking. Express a commitment to master the assigned role, add measurable value, automate repetitive manual tasks, and gradually earn opportunities on other projects. Illustrative example (replace with your mindset): 'I view every role as a chance to learn system fundamentals. If assigned to production support, I would focus on learning how our systems behave under real traffic, and I would write automated scripts to reduce recurring ticket volume. Excellence in my assigned responsibilities is the fastest way to earn trust for future architecture roles.'",
        "kp": ["Humility and commitment to team operational needs", "Recognizing learning value in testing and support (observability, debugging)", "Initiative to automate repetitive tasks within any assignment", "Professional reliability that builds trust with leadership"],
        "cm": ["Saying 'I am an AI engineer; I will resign if given support or testing work'", "Doing a sloppy job on uninteresting tasks out of resentment", "Claiming testing and support are beneath engineering graduates"],
        "fu": ["How would you use automation to improve efficiency in a repetitive support role?", "How does understanding testing make someone a significantly better software developer?"],
        "tags": ["adaptability", "support", "humility", "professionalism", "fresher"]
    },
    {
        "q": "What are your specific expectations from your engineering manager and team lead?",
        "sub": "Manager Relations",
        "d": "Beginner",
        "ans": "Interviewer is assessing: self-awareness, communication preferences, and whether you are easy to manage. Express expectations that emphasize growth, clear standards, and constructive feedback: 1) Clear goals and context (understanding why a feature matters to business), 2) Honest, timely constructive feedback (not waiting for annual reviews to point out growth areas), 3) Availability for unblocking and mentorship when independent avenues are exhausted, and 4) Autonomy once trust is established. Illustrative example (replace with your words): 'I value an engineering manager who sets clear expectations and business context, provides candid, regular feedback so I know where to improve, and gives me room to solve problems independently while being available to guide me when complex blockers arise.'",
        "kp": ["Clear expectations and business context for tasks", "Constructive, timely feedback to support professional growth", "Guidance on technical blind spots and architectural direction", "Autonomy balanced with supportive mentorship"],
        "cm": ["Expecting a manager to micromanage your daily hourly tasks", "Saying 'I expect my manager to leave me completely alone'", "Focusing on personal perks or hand-holding rather than professional development"],
        "fu": ["How do you prefer to receive critical feedback—in the moment or during scheduled 1-on-1s?", "What do you do if you feel your manager's instructions are vague or ambiguous?"],
        "tags": ["manager-relations", "expectations", "feedback", "growth"]
    },
    {
        "q": "What insightful questions do you have for me as the interviewer at the end of this round?",
        "sub": "Closing Questions",
        "d": "Beginner",
        "ans": "Interviewer is assessing: curiosity, depth of thought, and whether you are evaluating company fit. Never say 'I have no questions'. Ask 2 or 3 thoughtful, specific questions spanning engineering practices, team challenges, and career growth. Examples: 1) 'What does a typical release cycle look like on your team, and how are code reviews conducted?', 2) 'What is the biggest technical challenge your engineering team is actively solving this quarter?', 3) 'What distinguishes a fresher who ramps up exceptionally well in your team from someone who struggles?' Illustrative example (choose questions aligned with your role): 'I noticed your team recently migrated to [Architecture/Tool]. What was the biggest hurdle during that transition, and how has it impacted your daily deployment cadence?'",
        "kp": ["Always have 2-3 prepared questions; never say 'I have no questions'", "Ask about engineering culture, deployment cycles, and technical challenges", "Ask about expectations for freshers and success metrics in the first 6 months", "Demonstrates intellectual curiosity and proactive preparation"],
        "cm": ["Asking about salary, leaves, snacks, or benefits in a technical or managerial round", "Asking basic questions that could be answered by a 10-second Google search", "Saying 'No, you covered everything, I have no questions'"],
        "fu": ["Why is asking about the team's release cadence more insightful than asking about company culture?", "How do the interviewer's answers help you decide if this company is the right fit?"],
        "tags": ["closing-questions", "interviewer-questions", "curiosity", "fit"]
    },
    {
        "q": "Are you comfortable working in rotational shifts or weekend on-call support if required by project needs?",
        "sub": "Work Flexibility",
        "d": "Beginner",
        "ans": "Interviewer is assessing: flexibility, operational readiness, and alignment with Indian IT client service models (US/UK timezone support). For IT services companies and global SaaS products, shift rotations and on-call rosters are standard. Answer with honest, confident flexibility, affirming your willingness to support business continuity while asking professional questions about rotational schedules and compensation policies. Illustrative example (replace with your facts): 'Yes, I am comfortable working in rotational shifts or participating in on-call rotations. I understand that global enterprise systems require 24/7 reliability. During college project hackathons, I regularly worked late hours to meet delivery deadlines, and I am fully prepared to adapt to the team\\'s operational schedule.'",
        "kp": ["Clear, affirmative commitment to rotational shifts and operational continuity", "Understanding that enterprise clients require global timezone coverage", "Evidence of personal flexibility and adaptability", "Professional inquiry about shift rotation cadence"],
        "cm": ["Saying an outright 'No, I only work 9 to 5' (disqualifies candidate in many IT service drives)", "Overpromising that you can work 24/7 indefinitely without sleep", "Sounding bitter or reluctant about standard operational duties"],
        "fu": ["How do you manage your energy and sleep cycle when transitioning between day and night shifts?", "What is an incident on-call roster and how do engineers handle midnight alerts?"],
        "tags": ["shifts", "on-call", "flexibility", "it-services", "work-culture"]
    },
    {
        "q": "Are you willing to relocate to any of our operating offices across India (Bengaluru, Hyderabad, Pune, Chennai, Noida)?",
        "sub": "Relocation & Mobility",
        "d": "Beginner",
        "ans": "Interviewer is assessing: geographic mobility, personal independence, and availability for project allocation. Indian campus hiring drives often allocate freshers based on client project demand across regional tech hubs. Answer with an enthusiastic, unambiguous 'Yes', explaining that you view relocation as an exciting opportunity to experience a major tech hub, grow independently, and immerse yourself in the company's engineering ecosystem. Illustrative example (replace with your words): 'Yes, I am 100% willing to relocate to any office location including Bengaluru, Hyderabad, Pune, Chennai, or Noida. I see relocation as an essential step in my professional journey, allowing me to collaborate directly with senior mentors in major tech hubs and build my career independently.'",
        "kp": ["Unambiguous affirmative commitment to relocation across India", "Positive attitude viewing relocation as a career growth catalyst", "Preparedness for independent living in major metropolitan tech hubs", "Zero geographic friction during project allocation"],
        "cm": ["Saying 'I will only work in my hometown' unless the drive explicitly permits local-only hiring", "Showing hesitation or saying 'I need to ask my parents before I decide'", "Demanding permanent work-from-home when the role specifies on-site collaboration"],
        "fu": ["How soon after receiving the offer letter would you be able to relocate?", "What steps have you thought about for settling into a new city (housing, commute)?"],
        "tags": ["relocation", "mobility", "career-commitment", "fresher"]
    },
    {
        "q": "What is your understanding of employment service agreements (bonds) and notice periods in the Indian IT sector?",
        "sub": "Employment Policies",
        "d": "Beginner",
        "ans": "Interviewer is assessing: legal awareness, commitment, and realistic expectations regarding Indian placement policies. Many companies invest significant training capital in engineering freshers and utilize 1 to 2-year service agreements with reasonable training expense recovery clauses to ensure stability. Notice periods (typically 60 to 90 days) ensure smooth knowledge transfer and project continuity. Express that you have reviewed the policy, understand the rationale behind training investment protection, and are seeking a stable long-term platform to build foundational engineering skills rather than job-hopping. Illustrative example (replace with your stance): 'I understand that companies invest significant training resources and mentor time into fresh graduates, and service agreements provide mutual stability. My goal is to build strong, foundational engineering skills over several years with my first employer, so a standard service agreement aligns with my long-term career plans.'",
        "kp": ["Understanding of training investment protection rationale", "Commitment to long-term skill development over short-term job-hopping", "Awareness of standard notice period and transition protocols", "Mature, professional attitude toward standard company policies"],
        "cm": ["Reacting with shock or hostility to mention of a service agreement", "Signing agreements without reading or understanding financial terms", "Bluntly admitting that you plan to leave after 6 months for higher pay"],
        "fu": ["What factors would make you stay with an organization for 3+ years?", "Why do Indian companies maintain 60 to 90-day notice periods compared to 2 weeks in the US?"],
        "tags": ["bonds", "service-agreement", "notice-period", "retention", "it-policies"]
    },
    {
        "q": "How do you handle repetitive, tedious tasks that don't involve exciting new technologies?",
        "sub": "Work Ethic & Automation",
        "d": "Beginner",
        "ans": "Interviewer is assessing: discipline, attention to detail, and automation mindset. Real-world engineering involves repetitive data verification, test writing, manual deployments, or log audits. Explain that you approach repetitive tasks with two principles: 1) Precision: execute the task meticulously because business operations rely on accuracy, and 2) Automation: analyze the repetitive workflow to identify patterns and write scripts (Python, Bash, SQL) to automate or streamline it for the future. Illustrative example (replace with your experience): 'When tasked with manually verifying 200 question tags in our project, I didn't complain. I completed the immediate check carefully, but simultaneously wrote a 25-line Python validation script that automated the checks for all future imports. This turned a recurring 2-hour chore into a 2-second command.'",
        "kp": ["Commitment to meticulous accuracy on unexciting tasks", "Proactive mindset: look for opportunities to automate via scripting", "Understanding that foundational operational discipline builds engineering trust", "Turning manual chores into reusable automated tools"],
        "cm": ["Complaining about 'boring work' and letting quality slip", "Refusing to do repetitive tasks because 'I want to build AI only'", "Spending 3 days building an over-engineered automation tool for a one-time 10-minute task"],
        "fu": ["How do you evaluate whether a repetitive task is worth automating (XKCD automation matrix)?", "What is one manual task in your college workflow that you automated?"],
        "tags": ["automation", "work-ethic", "discipline", "scripting", "productivity"]
    },
    {
        "q": "What makes an Indian IT service-based company (TCS, Infosys, Wipro, Accenture) different from a product-based tech startup?",
        "sub": "Industry Awareness",
        "d": "Intermediate",
        "ans": "1) Service-Based Companies (e.g., TCS, Infosys, Accenture): build and maintain software solutions for external enterprise clients across diverse global industries (banking, retail, healthcare). Scale: massive workforces (hundreds of thousands), formal training programs, established processes (ITIL, Agile), structured career ladders, and high stability. Revenue tied to billable client hours or managed service contracts. 2) Product-Based Tech Startups (e.g., Swiggy, Zerodha, early-stage SaaS): build, own, and iterate on their own proprietary software product. Scale: smaller teams, rapid iteration cycles, high ambiguity, broader individual ownership across the full stack, and higher risk/reward volatility. Both offer valuable paths: services provide structured global scale and domain diversity; startups provide fast-paced end-to-end product ownership.",
        "kp": ["Service-based: client-driven software, massive scale, structured training, process maturity", "Product-based: proprietary product ownership, rapid iteration, full-stack individual ownership", "Understanding different revenue engines (client billability vs product subscriptions/GMV)", "Ability to articulate why the specific company model aligns with your career stage"],
        "cm": ["Insulting service-based companies while interviewing at a service company", "Assuming service companies do zero technical innovation", "Using generic buzzwords without understanding business mechanics"],
        "fu": ["Why are client communication skills and domain knowledge exceptionally critical in service companies?", "How do billing models (Fixed Price vs Time & Materials) affect engineering delivery?"],
        "tags": ["service-vs-product", "tcs", "infosys", "startups", "industry-awareness"]
    },
    {
        "q": "What would you do if you finished all your assigned tasks early in a sprint?",
        "sub": "Proactive Initiative",
        "d": "Beginner",
        "ans": "Interviewer is assessing: proactiveness, team spirit, and continuous learning. A passive developer sits idle waiting for the next sprint. A high-performing developer takes positive initiative: 1) Verify: double-check your code, edge-case unit test coverage, and documentation, 2) Assist: check in with teammates or sprint backlog to see if peers are blocked or need help with code review, 3) Pay down tech debt: refactor messy code, improve test coverage, or update developer setup guides, and 4) Communicate: inform the team lead during standup that you have capacity to pull the next priority backlog ticket. Illustrative example (replace with your facts): 'Whenever I completed project milestones ahead of schedule, I first reviewed my code against edge cases, then asked my teammates if they needed testing support, and used remaining hours to research the upcoming sprint\\'s technology requirements.'",
        "kp": ["Verify personal deliverables and test coverage thoroughly first", "Offer assistance to unblock teammates or review pull requests", "Tackle low-priority technical debt, documentation, or test enhancements", "Inform team lead during standup of available capacity"],
        "cm": ["Going home early or browsing social media silently without telling anyone", "Taking on major unapproved architecture rewrites without consulting the lead", "Boasting to teammates about how fast you finished while they are struggling"],
        "fu": ["How do you help a struggling teammate without making them feel micromanaged or inadequate?", "What is the difference between pulling an approved backlog ticket vs inventing your own task?"],
        "tags": ["initiative", "teamwork", "sprint", "proactiveness"]
    },
    {
        "q": "How do you handle constructive criticism and code review feedback that rejects your pull request?",
        "sub": "Code Reviews & Feedback",
        "d": "Beginner",
        "ans": "Interviewer is assessing: ego separation, receptiveness to learning, and code review maturity. Code reviews are not personal attacks; they are the primary mechanism for code quality and mentorship. Explain that you: 1) Separate your ego from your code ('I am not my code'), 2) Read the reviewer's feedback objectively to understand the underlying concern (performance, readability, team conventions, security), 3) Ask clarifying questions if the suggestion is unclear, and 4) Implement the requested changes promptly with gratitude for the senior engineer's review time. Illustrative example (replace with your experience): 'When a senior peer rejected my pull request due to an unindexed query and missing error handling, I didn't feel discouraged. I thanked him for catching the flaw before deployment, studied his suggested pattern, updated the code, and added a test case. It was one of the fastest learning moments I had.'",
        "kp": ["Ego separation: 'I am not my code'; feedback evaluates code quality, not self-worth", "Code reviews are free mentorship from experienced engineers", "Seek to understand the root engineering rationale behind reviewer comments", "Respond promptly, update pull requests, and express appreciation"],
        "cm": ["Taking code review rejections personally or getting into heated comment arguments on GitHub", "Ignoring reviewer comments and merging the pull request anyway", "Becoming hesitant to write code out of fear of future review feedback"],
        "fu": ["What do you do if two senior reviewers give contradictory feedback on your pull request?", "How do you give constructive, polite feedback when reviewing someone else's code?"],
        "tags": ["code-reviews", "feedback", "humility", "growth", "collaboration"]
    },
    {
        "q": "What is your approach to maintaining work-life balance and preventing burnout in demanding software roles?",
        "sub": "Well-being & Burnout",
        "d": "Beginner",
        "ans": "Interviewer is assessing: sustainable productivity, self-discipline, and emotional maturity. High performance over a multi-year engineering career requires sustainable work habits, not chronic 80-hour panic sprints. Explain your self-management habits: 1) Clear prioritization during work hours (focusing on high-impact deliverables without constant multitasking), 2) Intentional boundaries (disconnecting after work to recharge), 3) Regular physical exercise, hobbies, and sleep hygiene, and 4) Communicating early with leads when workload bottlenecks threaten sustainability before reaching crisis burnout. Illustrative example (replace with your habits): 'I maintain productivity by blocking focused deep-work hours for coding and keeping my daily priorities clear. Outside work, I stay active through [Sport/Hobby/Reading], which clears my head and allows me to return to engineering problems with fresh creative problem-solving energy every morning.'",
        "kp": ["Sustainable high performance over chronic frantic burnout", "Time management: focused deep-work blocks during work hours", "Healthy physical and mental recharge habits outside work", "Proactive communication with managers when workload exceeds capacity"],
        "cm": ["Boasting that you never sleep and code 18 hours every day (signals poor time management and high burnout risk)", "Saying you refuse to ever put in extra effort during critical deployment releases", "Having zero interests or outlets outside of computer screens"],
        "fu": ["How do you handle high-pressure crunch periods right before major client product launches?", "What early warning signs tell you that you are approaching mental exhaustion?"]
    },
    {
        "q": "What are your salary expectations as an engineering fresher joining our organization?",
        "sub": "Salary & Compensation",
        "d": "Beginner",
        "ans": "Interviewer is assessing: realistic market expectations, professional tone, and salary negotiation maturity. For campus hiring drives and entry-level engineering roles, compensation is typically standardized according to company salary bands. Express that your primary focus is joining a reputed engineering organization, receiving high-quality mentorship, and launching your career, while trusting that the company offers competitive, industry-standard compensation for fresher roles. Illustrative example (replace with your words): 'My primary priority is launching my engineering career with an organization where I can learn from experienced mentors and contribute to meaningful projects. Based on my research on industry standards for entry-level [Role] positions in your company, I am confident that your offer will be competitive and aligned with your standardized salary bands.'",
        "kp": ["Acknowledge standardized fresher compensation bands in campus/entry drives", "Prioritize career foundation, mentorship, and learning over short-term haggling", "Reference industry research and fair compensation benchmarks", "Confident, professional, and non-confrontational tone"],
        "cm": ["Demanding an arbitrary, unrealistic number with zero market research", "Saying 'money doesn't matter at all to me' (sounds insincere)", "Refusing to discuss compensation or being aggressive in an initial interview"],
        "fu": ["What components of compensation (base salary, performance bonus, PF, health insurance) do you value most?", "What would you do if you received an offer from another company with a slightly higher salary?"]
    },
    {
        "q": "What if you receive an offer from a competitor with a 15% higher salary after joining our company?",
        "sub": "Loyalty & Career Vision",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: stability, career vision, and whether you are a chronic job-hopper who jumps for minor short-term cash. Explain that you view career decisions through long-term skill acquisition and organizational stability, not marginal short-term salary increments. Jumping companies prematurely disrupts learning curves, damages professional reputation, and resets mentorship trust. If your current company provides strong technical growth, fair mentorship, and a clear promotion trajectory, staying and building mastery yields far greater long-term earnings than frequent lateral moves. Illustrative example (replace with your words): 'I evaluate my career based on the steepness of my learning curve, the quality of mentorship, and the impact of the projects I am building. A 15% increment does not justify abandoning a project where I am growing rapidly. As long as I am learning, contributing, and being fairly compensated according to my performance, I prefer to build a strong multi-year track record with one organization.'",
        "kp": ["Long-term skill compounding and mentorship valued over minor short-term increments", "Frequent early job-hopping damages professional credibility and resumes", "Loyalty grounded in mutual growth, learning, and fair evaluation", "Confident commitment to finishing what you start"],
        "cm": ["Saying 'I will definitely leave immediately for any higher offer'", "Pretending you would stay forever even if severely underpaid and mistreated (insincere)", "Showing that salary is your sole decision-making metric"],
        "fu": ["Under what circumstances would you consider leaving an organization?", "How does staying with an organization for 3 years accelerate leadership opportunities compared to 1-year hops?"]
    },
    {
        "q": "How do you manage multiple competing priorities and deadlines when three different stakeholders ask for help at once?",
        "sub": "Prioritization Frameworks",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: task management under pressure, Eisenhower Matrix prioritization, and communication clarity. Explain your framework: 1) Clarify urgency vs importance: determine which task has direct production or customer-blocking impact, 2) Evaluate deadlines and estimated time required for each deliverable, 3) Align with your direct manager or team lead ('Manager, I currently have Task A from Stakeholder 1 and Task B from Stakeholder 2. Which should take precedence for our sprint goals?'), and 4) Communicate timelines proactively to all stakeholders so expectations are managed without silent delays. Illustrative example (replace with your real experience): 'When our college project had simultaneous submissions for UI design, backend integration, and the project report, I used an Eisenhower matrix to prioritize backend endpoints that unblocked the team, agreed on delivery order with my peers, and kept our guide informed of our phased delivery schedule.'",
        "kp": ["Prioritize by business impact and customer urgency (Eisenhower Matrix)", "Align with direct manager to resolve conflicting stakeholder demands", "Communicate revised realistic timelines proactively to all requesters", "Avoid multitasking chaos by executing prioritized tasks sequentially"],
        "cm": ["Saying 'Yes' to everyone immediately and failing to deliver any task on time", "Hiding the conflict and hoping deadlines magically resolve themselves", "Ignoring a stakeholder completely without explaining why their task is queued"],
        "fu": ["How do you say 'No' or 'Not right now' to a senior stakeholder professionally?", "What tools do you use to track your personal daily priorities (Jira, Trello, Notion, Todoist)?"]
    },
    {
        "q": "How do you handle cross-cultural communication when working with international clients (US, UK, Europe, Australia)?",
        "sub": "Cross-Cultural Communication",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: global professional communication skills, cultural sensitivity, and client etiquette in the Indian IT export sector. Key principles: 1) Clarity and Directness: western clients prefer clear, concise, direct communication; avoid excessive filler, ambiguous answers, or saying 'yes' when you mean 'I understand, but it\\'s not possible', 2) Timezone Discipline: respect meeting punctuality and asynchronous updates, 3) Written Documentation: follow up verbal meetings with clear written summaries and action items, and 4) Professional Tone: maintain polite, collaborative, and confident dialogue without subservience or aggression. Illustrative example (replace with your words): 'When collaborating with international contributors on an open-source project, I learned to write crisp PR summaries, state assumptions directly rather than leaving ambiguity, and accommodate timezone offsets for synchronous reviews.'",
        "kp": ["Direct, transparent communication without ambiguous 'Indian head nod' yes-saying", "Punctuality and respect for international business timezones", "Follow up verbal discussions with written documentation and action items", "Confidence and mutual respect in client interactions"],
        "cm": ["Saying 'Yes' to an impossible client deadline out of politeness, causing delivery failure", "Using local regional idioms or slang that international clients cannot understand", "Failing to send written follow-up notes after client calls"],
        "fu": ["Why is saying 'No, but here is what we can do' far more respected by US/European clients than false promises?", "How do you handle strong linguistic accents during client conference calls?"]
    },
    {
        "q": "What is your philosophy on documentation? How do you balance writing code with writing documentation?",
        "sub": "Documentation Culture",
        "d": "Beginner",
        "ans": "Interviewer is assessing: engineering maturity and team empathy. Undocumented code is technical debt; if code cannot be understood or deployed by another engineer, it is incomplete. Good documentation balances: 1) Self-documenting code: clean naming conventions, type hints, and modular functions that explain 'what' the code does, 2) Comments that explain 'why' (trade-offs, non-obvious business logic, bug workarounds), and 3) High-level system docs: clean READMEs, API Swagger specs, and architecture flowcharts that allow a new developer to onboard in under an hour. Illustrative example (replace with your practice): 'In our repository, I ensured every API had Pydantic models generating automatic OpenAPI docs, and wrote a clean README with step-by-step Docker commands. When another student cloned our repo and launched it in 5 minutes without asking for help, it proved that 30 minutes of documentation saved hours of onboarding friction.'",
        "kp": ["Undocumented code is incomplete technical debt", "Code explains WHAT; comments and documentation explain WHY", "Automated API documentation (Swagger/OpenAPI) and clean README setup guides", "Documentation is a courtesy to teammates and future maintainers"],
        "cm": ["Writing zero documentation claiming 'my code is self-documenting'", "Writing obvious, useless comments like `# increment x: x += 1`", "Letting documentation go stale and contradictory as code changes"],
        "fu": ["What tools automate documentation generation in modern software engineering?", "How do you ensure documentation stays updated when APIs change in continuous deployment?"]
    },
    {
        "q": "Where do you see yourself in 3 to 5 years in our engineering organization?",
        "sub": "Career Vision",
        "d": "Beginner",
        "ans": "Interviewer is assessing: career ambition, realistic growth expectations, and retention potential. Outline a credible progression: 1) In years 1-2: achieve deep technical mastery of the stack, become an independent, reliable feature contributor, and master production debugging, 2) In years 3-4: step up as a Senior Software Engineer taking ownership of component architecture, mentoring junior freshers, and collaborating on system design, and 3) By year 5: either evolve into a Technical Lead / Staff Engineer driving architectural decisions or an Engineering Manager guiding team execution, depending on where your strengths align. Illustrative example (replace with your personal goals): 'In 3 years, I see myself as a senior contributor who has mastered our production architecture and can be trusted with mission-critical feature releases. By year 5, I want to mentor incoming engineering cohorts, contribute to architectural design choices, and bridge the gap between technical execution and business product goals.'",
        "kp": ["Credible 3-5 year progression from independent contributor to senior/lead", "Emphasis on technical depth, production reliability, and mentoring others", "Realistic understanding of engineering hierarchy (Junior -> Senior -> Lead)", "Alignment with the company's long-term growth opportunities"],
        "cm": ["Saying 'I want to be the CEO in 3 years' (unrealistic arrogance)", "Saying 'I haven't thought about it at all' (zero vision)", "Saying 'I want to leave for an MBA in 2 years' (disqualifies candidate for technical investment)"],
        "fu": ["What is the difference between the Individual Contributor (IC) track and the Management track in tech?", "What technical skills do you need to develop to become an effective Senior Engineer?"]
    }
]

PART2 = [
    {
        "q": "What would you do if you noticed a teammate committing sensitive API keys or database passwords to a public Git repository?",
        "sub": "Security Incident",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: security urgency, procedural judgment, and diplomatic intervention. Exposed credentials can be scraped by automated bots within seconds. Correct protocol: 1) Act immediately: notify the teammate and team lead directly and urge an immediate credential rotation/invalidation on the cloud provider or service console (deleting the Git commit alone is insufficient because credentials remain in Git history and bot caches), 2) Remove from history: rewrite Git history using `git-filter-repo` or BFG Repo-Cleaner to purge the sensitive file, 3) Add to .gitignore, and 4) Institutionalize prevention: install automated secret-detection pre-commit hooks (TruffleHog, Gitleaks) to block secrets from ever reaching commits. Illustrative example (replace with your words): 'When a classmate committed an AWS key during our project, I immediately alerted him to revoke the key in the AWS console first. We then scrubbed the repository history using git filter-repo and added pre-commit secret detection hooks to prevent future leaks.'",
        "kp": ["Rotate and invalidate exposed credentials immediately on the service console", "Scrub Git history using specialized tools (git-filter-repo / BFG)", "Add secrets files to .gitignore", "Install automated secret-scanning pre-commit hooks (Gitleaks / TruffleHog)"],
        "cm": ["Thinking that making a new commit that deletes the file hides the secret (it remains in git history)", "Waiting until tomorrow's standup to report an exposed active credential", "Publicly shaming the teammate instead of focusing on immediate containment"],
        "fu": ["Why is revoking the secret key more urgent than cleaning the Git commit history?", "How do environment secrets managers (AWS Secrets Manager, HashiCorp Vault) eliminate local secret files?"]
    },
    {
        "q": "How would you handle a situation where a critical software defect is discovered in production late on a Friday evening?",
        "sub": "Incident Response",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: incident triage, calm execution under pressure, and production protocol awareness. Follow the standard incident management lifecycle: 1) Triage severity: determine if the defect is a Sev-1 (critical outage, data loss, payment failure) requiring immediate intervention or a Sev-3 (minor visual glitch) that can be scheduled safely for Monday morning, 2) If critical: declare an incident, notify on-call leads and stakeholders via designated channels (Slack/PagerDuty), 3) Mitigate immediately: prefer safe rollback to the previous stable release over rushing an untested 'hotfix' into production under stress, 4) Verify stability, and 5) Schedule a blameless post-mortem for the following week to determine root causes. Illustrative example (replace with your stance): 'I would first evaluate the severity. If customer data or payments were blocked, I would alert the on-call engineer and support a rollback to the last known healthy build. Rushing untested hotfix code on Friday night introduces more bugs; rolling back restores service safely while we investigate the root cause properly.'",
        "kp": ["Triage severity (Sev-1 critical vs Sev-3 non-blocking)", "Prefer rolling back to last known stable build over rushing untested hotfixes", "Communicate status transparently via incident channels", "Conduct a blameless post-mortem during normal business hours"],
        "cm": ["Deploying rushed, untested code directly to production in panic mode", "Ignoring the issue and going home for the weekend hoping nobody notices", "Failing to notify customer support and stakeholders of ongoing production outages"],
        "fu": ["What is the difference between a Rollback and a Rollforward deployment fix?", "What key sections belong in a blameless post-mortem report?"]
    },
    {
        "q": "What is your approach to giving feedback to a teammate whose work is consistently below quality expectations?",
        "sub": "Peer Feedback",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: empathy, peer leadership, and direct professional communication. Giving critical peer feedback requires tact and concrete evidence: 1) Address privately: never criticize a teammate publicly in front of the group or in Slack channels, 2) Focus on the work, not personality: use specific examples of objective issues (e.g., 'In the last two PRs, unit tests were missing and edge cases caused staging build failures') rather than vague judgments ('You are careless'), 3) Listen: ask if they are facing personal blockers, lack of clarity, or need pairing, and 4) Offer collaborative support: offer to pair-program on one ticket to establish quality conventions together. Illustrative example (replace with your experience): 'When a teammate struggled with code quality on our capstone project, I spoke with him privately. I pointed out specific staging bugs, listened to where he was stuck, and spent two hours pairing with him on testing. His subsequent PRs improved dramatically because the feedback was constructive and supportive.'",
        "kp": ["Deliver feedback privately in 1-on-1 settings, never in public channels", "Anchor feedback in objective facts, error logs, and specific PRs", "Listen with empathy to identify underlying blockers or knowledge gaps", "Offer collaborative pairing to establish quality standards together"],
        "cm": ["Venting complaints to other teammates behind their back", "Attacking the person rather than the objective code output", "Escalating directly to the manager before having a private conversation with the peer"],
        "fu": ["When is it appropriate to escalate peer quality issues to the team lead or manager?", "What is the SBI (Situation-Behavior-Impact) feedback model?"]
    },
    {
        "q": "How do you evaluate and choose which third-party open-source libraries are safe and suitable to import into a project?",
        "sub": "Open Source Hygiene",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: dependency hygiene, software supply-chain security, and licensing awareness. Blindly running `npm install` or `pip install` introduces security vulnerabilities and legal liability. Evaluation criteria: 1) Open Source License: check for permissive licenses (MIT, Apache 2.0, BSD); beware restrictive copyleft licenses (GPL, AGPL) that can force proprietary commercial codebases to become open-source, 2) Health & Maintenance: check commit frequency, open issue resolution speed, and recent releases, 3) Popularity & Community: download counts, GitHub stars, and corporate sponsorship, 4) Security Audit: check for known CVE vulnerabilities using tools like Snyk or `npm audit`, and 5) Dependency Tree: inspect whether importing a simple utility pulls in 500 transitive sub-dependencies. Illustrative example (replace with your experience): 'Before adding libraries to our backend, I verified they had MIT or Apache 2.0 licenses, active commits within the last 3 months, and zero critical vulnerabilities on Snyk, ensuring our project didn\\'t inherit licensing risks or security liabilities.'",
        "kp": ["License compatibility check (MIT/Apache vs restrictive GPL/AGPL copyleft)", "Maintenance activity: recent commits, releases, and issue resolution cadence", "Security vulnerability audits using automated scanners (Snyk, Dependabot)", "Evaluate transitive dependency bloat and bundle size impact"],
        "cm": ["Importing unvetted libraries with restrictive AGPL licenses into commercial enterprise products", "Using abandoned libraries with zero commits in 4 years and known unpatched CVEs", "Importing massive 50MB libraries for a single trivial 5-line utility function"],
        "fu": ["What is a supply-chain attack (e.g., malicious npm package typosquatting)?", "What is the difference between permissive open-source licenses and copyleft licenses?"]
    },
    {
        "q": "What would you do if you were asked to work on a feature that you suspect could violate user privacy or consumer ethics?",
        "sub": "Ethical Engineering",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: ethical integrity, professional courage, and constructive escalation. Software engineers have an ethical responsibility to protect user privacy (GDPR, DPDP Act in India) and security. Protocol: 1) Verify facts: ensure you thoroughly understand the feature requirements and are not jumping to false assumptions, 2) Raise questions professionally: ask for clarification on data privacy, consent mechanisms, and legal compliance in writing ('How are we obtaining explicit user consent for tracking this location data according to privacy laws?'), 3) Propose ethical alternatives: offer privacy-preserving architectures (data anonymization, client-side aggregation, opt-in toggles), and 4) Escalate through official channels (compliance team, security officer, or HR ethics hotline) if unethical directives persist. Illustrative example (replace with your principles): 'If asked to track user data without consent, I would politely raise the legal and privacy compliance risks with my lead, reference standard regulations, and suggest an opt-in consent model that achieves business analytics goals while respecting user trust.'",
        "kp": ["Verify facts before making ethical accusations", "Raise concerns professionally focusing on legal risks, compliance, and user trust", "Propose privacy-preserving engineering alternatives (anonymization, opt-in)", "Escalate through official compliance and ethics channels when necessary"],
        "cm": ["Blindly implementing unethical features saying 'I was just following orders'", "Leaking confidential company code to social media before raising issues internally", "Accusing colleagues of malicious intent without understanding regulatory requirements"],
        "fu": ["What is India's Digital Personal Data Protection (DPDP) Act and how does it mandate user consent?", "What is Privacy by Design in modern software architecture?"]
    },
    {
        "q": "What is the difference between an Agile Scrum framework and a traditional Waterfall project methodology?",
        "sub": "Software Methodology",
        "d": "Beginner",
        "ans": "1) Waterfall (Linear-Sequential): phases progress strictly in sequence: Requirements -> Design -> Implementation -> Verification -> Maintenance. Working software is delivered only at the very end of the multi-month cycle. Strengths: clear contracts, rigid documentation, predictable milestones. Weaknesses: highly inflexible to changing customer requirements; discoveries of design flaws happen late during testing when fixes are expensive. 2) Agile Scrum (Iterative-Incremental): work is organized into short timeboxed cycles called Sprints (typically 2 weeks). Cross-functional teams plan, build, test, and deliver shippable increments of software every sprint. Scrum ceremonies include Sprint Planning, Daily Standups, Sprint Review (demo), and Retrospective. Strengths: rapid adaptation to customer feedback, early defect detection, and continuous value delivery.",
        "kp": ["Waterfall: linear, rigid, deliverables produced at project conclusion", "Agile: iterative, flexible, working software delivered in 2-week sprints", "Scrum ceremonies: Planning, Daily Standup, Review (Demo), Retrospective", "Scrum roles: Product Owner (backlog priority), Scrum Master (process coach), Developers"],
        "cm": ["Assuming Agile means 'no documentation and no planning'", "Running Waterfall in 2-week increments and calling it Agile", "Treating Daily Standup as an interrogation rather than a quick sync"],
        "fu": ["What is the primary purpose of a Sprint Retrospective meeting?", "What is the difference between Kanban (continuous flow) and Scrum (sprints)?"]
    },
    {
        "q": "What is the purpose of the Daily Standup meeting in Scrum and what are the three standard questions?",
        "sub": "Scrum Ceremonies",
        "d": "Beginner",
        "ans": "The Daily Standup is a short, timeboxed (typically 15-minute) synchronization meeting for the development team to align on sprint progress, coordinate collaboration, and identify blockers. It is not an executive status report to a manager. Each developer briefly answers three standard questions: 1) What did I accomplish yesterday that helped the team meet the sprint goal? 2) What do I plan to accomplish today? 3) What blockers or impediments are slowing me down or preventing progress? Detailed technical problem-solving is taken offline after the standup ('parking lot') with relevant team members to keep the meeting fast and energized.",
        "kp": ["Timeboxed 15-minute synchronization, not a detailed technical design debate", "Three questions: What I completed yesterday, What I will do today, What blockers exist", "Identifies impediments early so team leads can unblock engineers", "Deep technical discussions deferred to offline pairing sessions"],
        "cm": ["Turning standup into a 45-minute architectural debate", "Reporting micro-details like 'I opened my laptop and checked emails'", "Hiding blockers out of fear or embarrassment, delaying the sprint"],
        "fu": ["How do you effectively describe a blocker during standup without derailing the meeting?", "What role does the Scrum Master play in resolving blockers identified in standup?"]
    },
    {
        "q": "How do you prepare for your very first technical code deployment to a production environment?",
        "sub": "Production Readiness",
        "d": "Intermediate",
        "ans": "Deploying code to real users for the first time requires disciplined preparation: 1) Pre-Deployment Verification: ensure all unit and integration tests pass green in CI, run migrations on a staging replica database, and verify environment variable configs, 2) Deployment Strategy: coordinate with a senior engineer, deploy during scheduled low-traffic maintenance windows, and use zero-downtime deployment patterns (Blue-Green or Canary), 3) Monitoring & Observability: tail live server logs and watch error rate metrics (Datadog, Sentry, CloudWatch) immediately following release, and 4) Rollback Readiness: have an automated or documented rollback plan ready to execute instantly if error rates spike. Illustrative example (replace with your steps): 'For our first production release, I reviewed the migration plan with my senior peer, tested the deployment script on our staging container, monitored live logs for 30 minutes post-deploy, and verified key user workflows manually.'",
        "kp": ["Verify passing CI tests and validate database migrations on staging first", "Deploy with senior peer guidance during low-traffic windows", "Active monitoring of error rates, latency, and logs immediately post-release", "Clear, practiced rollback strategy ready for instant execution if issues emerge"],
        "cm": ["Deploying directly to production on Friday afternoon right before leaving the office", "Deploying without checking if database migrations are backward compatible", "Closing the laptop and assuming everything works without monitoring live logs"],
        "fu": ["What is a Blue-Green deployment and how does it achieve zero-downtime releases?", "What is a Canary release and how does it limit the blast radius of new bugs?"]
    },
    {
        "q": "What is the difference between a Junior Software Engineer, a Senior Software Engineer, and a Tech Lead?",
        "sub": "Engineering Levels",
        "d": "Intermediate",
        "ans": "1) Junior Software Engineer (L1/L2): focuses on execution and learning; works on well-defined tasks and features with guidance; primary growth is developing technical independence, code quality, and debugging proficiency. 2) Senior Software Engineer (L3/L4): handles ambiguity; designs end-to-end features, anticipates architectural trade-offs and edge cases, writes robust tests, and actively mentors juniors through thorough code reviews. Responsible for system reliability and technical quality across their module. 3) Tech Lead: sets technical vision for a team, bridges engineering with product management, makes difficult architectural compromises, breaks high-level roadmaps into actionable sprint tasks, and unblocks engineers. Growth is measured from 'how well I code' to 'how well my team delivers'.",
        "kp": ["Junior: executes well-defined tasks, builds technical independence, learns conventions", "Senior: manages ambiguity, designs architectures, anticipates trade-offs, mentors juniors", "Tech Lead: aligns engineering with product, unblocks team, sets technical vision", "Progression transitions from individual output to team multiplier impact"],
        "cm": ["Thinking seniority is measured purely by years of experience rather than problem-solving scope", "Assuming senior engineers code 10x faster rather than making better architectural decisions", "Believing technical leads only manage people without technical depth"],
        "fu": ["What does it mean for an engineer to be a 'team multiplier'?", "How do the engineering expectations change when moving from campus hire to mid-level?"]
    },
    {
        "q": "How do you stay up-to-date with fast-evolving technologies in software engineering and AI?",
        "sub": "Continuous Learning",
        "d": "Beginner",
        "ans": "Interviewer is assessing: intellectual curiosity, self-directed learning, and personal information filtering. Technology evolves rapidly, especially in AI and web frameworks. Outline a disciplined learning routine: 1) Primary Sources: reading official documentation, release notes, and engineering blogs from top tech companies (Meta Engineering, Uber Engineering, Netflix TechBlog), 2) Hands-On Building: building small weekend projects or testing new libraries rather than just reading passively, 3) Curated Newsletters & Communities: Hacker News, GitHub Trending, arXiv papers, and reputable technical newsletters (ByteByteGo, Pragmatic Engineer), and 4) Podcasting / Technical Talks: watching conference talks (PyCon, AWS re:Invent). Illustrative example (replace with your routine): 'I follow engineering blogs like Uber and Cloudflare to understand real-world scale architectures, and I reserve 3 hours every weekend to build small experiments testing new tools like FastAPI or LangChain.'",
        "kp": ["Curated high-signal sources: official docs and top engineering tech blogs", "Hands-on implementation over passive video watching", "Disciplined weekly routine for exploring new tools", "Focus on enduring foundational principles (networking, databases, OS) alongside hype tools"],
        "cm": ["Relying exclusively on 30-second TikTok or Instagram coding reels for technical knowledge", "Chasing every single new hype library without understanding core computer science fundamentals", "Claiming 'I don't need to learn anything new because college taught me everything'"],
        "fu": ["How do you filter high-signal engineering content from shallow marketing hype?", "What is one technical book or engineering article that fundamentally changed how you think?"]
    },
    {
        "q": "What would you do if you were assigned a legacy codebase with zero documentation, spaghetti code, and no unit tests?",
        "sub": "Legacy Code",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: resilience, methodical reverse-engineering, and working with imperfect real-world systems. Most enterprise software is legacy. Strategy: 1) Resist the urge to rewrite: complete rewrites introduce massive regressions and cost millions, 2) Map the system: trace entry points (routes, controllers), set up logging, and map input-output boundaries, 3) Characterization Tests: write black-box end-to-end integration tests that capture CURRENT behavior (even bugs) to create a safety net before touching code, 4) Boy Scout Rule: leave the code slightly cleaner than you found it on every ticket, refactoring incrementally within small, tested pull requests, and 5) Document as you go: write setup guides and architectural diagrams for the next engineer. Illustrative example (replace with your experience): 'When working on an inherited college project codebase with no docs, I first wrote end-to-end tests to establish a baseline of existing behavior. I then refactored one module at a time while adding docstrings, turning an unmaintainable script into a clean, testable system.'",
        "kp": ["Resist demanding an immediate full rewrite; respect business value of legacy code", "Write Characterization Tests to capture current behavior before refactoring", "Apply the Boy Scout Rule: clean up code incrementally during feature work", "Document architecture, dependencies, and environment setup as you learn"],
        "cm": ["Demanding an immediate full rewrite from scratch (classic junior anti-pattern)", "Refactoring large legacy modules without any automated tests, breaking production", "Complaining endlessly about previous developers' code quality instead of improving it"],
        "fu": ["What is a Characterization Test (Golden Master test) in legacy code refactoring?", "What is the Strangler Fig pattern for incrementally replacing legacy systems?"]
    },
    {
        "q": "What is the importance of code reviews from the perspective of both the author and the reviewer?",
        "sub": "Engineering Culture",
        "d": "Beginner",
        "ans": "Code reviews are a vital quality gate and knowledge-sharing ritual: 1) Author Perspective: acts as a safety net catching edge cases, performance bugs, and security oversights before production; provides tailored mentorship from senior peers; forces the author to write clean, self-documenting code with clear PR descriptions. 2) Reviewer Perspective: helps maintain architectural consistency and coding standards across the repository; shares knowledge so multiple engineers understand the new code (increasing bus factor); offers opportunities to learn novel techniques from teammates. It fosters a collective ownership culture where the entire team is responsible for codebase health.",
        "kp": ["Quality gate: catches bugs, security flaws, and performance regressions before deploy", "Knowledge sharing: eliminates single points of failure (increases Bus Factor)", "Mentorship vehicle for continuous engineering learning", "Fosters collective code ownership rather than isolated silos"],
        "cm": ["Treating code reviews as a rubber-stamp approval without actually inspecting the code", "Submitting massive 2,000-line pull requests that are impossible to review effectively", "Using harsh, sarcastic, or demanding language in code review comments"],
        "fu": ["What is an ideal pull request size to ensure thorough and effective code reviews?", "What is the 'Bus Factor' in software engineering team resilience?"]
    },
    {
        "q": "What would you do if your software build fails or CI pipeline breaks right before a scheduled team demo?",
        "sub": "High-Pressure Composure",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: emotional composure, triage under pressure, and pragmatic recovery. Panic worsens technical crises. Protocol: 1) Stay calm and communicate: inform the team lead immediately so expectations can be set, 2) Inspect CI logs: look at the exact failing step (lint error, failed unit test, missing environment variable, dependency timeout) to isolate the failure fast, 3) Revert to last green commit: if the fix is non-trivial, revert to the last passing build immediately rather than hacking code in panic, and 4) Demo from stable environment: conduct the demo using the stable staging environment or last verified build while debugging continues offline. Illustrative example (replace with your experience): 'When our build failed 15 minutes before our final project presentation due to an API timeout, I didn't panic. I checked the logs, identified that a mock server was down, reverted to our local cache fixture, and delivered a smooth presentation without the evaluators ever knowing there was a crisis.'",
        "kp": ["Maintain emotional composure; panic creates careless mistakes", "Inspect logs methodically to identify the exact failing step", "Revert to the last known stable green build to secure the demo", "Transparent communication with team lead regarding status"],
        "cm": ["Hacking code live on the main branch minutes before a presentation without testing", "Freezing in panic and failing to notify the team", "Blaming CI tools or teammates publicly"],
        "fu": ["How do automated staging environments prevent demo day failures?", "What is a 'pre-flight checklist' before presenting technical demos?"]
    },
    {
        "q": "How do you handle technical disagreements during sprint planning or architectural discussions?",
        "sub": "Collaboration & Consensus",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: collaborative consensus-building and engineering maturity. Disagreements in system design are normal and healthy when handled constructively: 1) Ground arguments in objective criteria: evaluate options against specific project requirements (latency SLAs, development time, scalability, maintenance cost) rather than personal aesthetic preference, 2) Build quick Proof-of-Concepts (POCs): if the team is split between two architectures, spend a timeboxed 2-hour session benchmarking both with real data, 3) Involve senior guidance: present the trade-offs to the tech lead or architect for final arbitration, and 4) Commit fully: once a decision is finalized, execute the chosen architecture with full commitment without lingering resentment. Illustrative example (replace with your experience): 'When our team debated between SQL and MongoDB for our capstone database, we listed our data access patterns. Seeing that 90% of our queries required relational joins, the data clearly pointed to SQL, allowing us to align quickly without emotional arguments.'",
        "kp": ["Anchor debates in objective project requirements and performance metrics", "Use quick, timeboxed Proof-of-Concepts (POCs) to let empirical data decide", "Involve technical leadership for arbitration when consensus stalls", "Commit fully to the chosen path once decided"],
        "cm": ["Turning technical trade-off debates into personal emotional feuds", "Passive-aggressively dragging your feet after your preferred architecture wasn't chosen", "Avoiding speaking up when you identify a genuine architectural flaw out of fear of conflict"],
        "fu": ["What is an Architecture Decision Record (ADR) and how does it document design consensus?", "How do you distinguish between bike-shedding (arguing over trivial details) and critical architectural decisions?"]
    },
    {
        "q": "What is the difference between working on an open-source project versus working on an internal enterprise codebase?",
        "sub": "Engineering Environments",
        "d": "Intermediate",
        "ans": "1) Open-Source Software (OSS): public visibility, decentralized asynchronous collaboration across global timezones, highly diverse volunteer contributors, consensus-driven governance, and rigorous automated CI/linting checks because anyone can submit pull requests. High emphasis on public documentation and backward compatibility. 2) Internal Enterprise Codebase: private proprietary repositories, co-located or coordinated sprint teams, clear organizational hierarchy and managerial decision-makers, direct access to product managers and internal stakeholders, and security/compliance boundaries (NDAs, SOC2, GDPR). Both share core engineering principles (Git, code reviews, testing, clean code), but enterprise software moves along business roadmaps and profit incentives.",
        "kp": ["Open source: public, asynchronous, decentralized, volunteer community, consensus", "Enterprise: private, sprint roadmaps, clear hierarchy, business deadlines, compliance", "OSS requires exceptional self-documenting pull requests and issue descriptions", "Enterprise software balances business speed with technical debt management"],
        "cm": ["Assuming open-source software has lower quality standards than enterprise code (top OSS often has higher standards)", "Sharing confidential enterprise code or proprietary logic on public forums", "Not knowing how pull requests and issues work on GitHub"],
        "fu": ["How does contributing to open-source software accelerate a fresher's engineering credibility?", "What is an InnerSource model within large enterprise engineering organizations?"]
    },
    {
        "q": "What steps do you take to secure your local development environment and prevent data leaks?",
        "sub": "Workplace Security",
        "d": "Beginner",
        "ans": "Interviewer is assessing: security hygiene and enterprise compliance. Securing local environments prevents security breaches: 1) Never store plain-text secrets or production API keys in local scripts; use `.env` files strictly added to `.gitignore`, 2) Enforce strong unique passwords and Multi-Factor Authentication (MFA) across all developer accounts (GitHub, AWS, corporate email), 3) Keep OS, IDE, and developer packages updated with security patches, 4) Never download unverified binaries, cracked software, or run curl-to-bash scripts from unknown sites, and 5) Lock laptops when stepping away from the desk and adhere to company VPN / disk encryption policies (BitLocker / FileVault). Illustrative example (replace with your habits): 'I use .env files with .gitignore templates, enable hardware MFA on my GitHub and email accounts, and keep my machine updated. I treat corporate data with strict confidentiality, ensuring no proprietary code is uploaded to personal cloud drives.'",
        "kp": ["MFA / 2FA enabled on all developmental and cloud accounts", ".env files strictly excluded from Git tracking via .gitignore", "Full disk encryption (BitLocker) and locking screens when away from desk", "Strict compliance with corporate security and data handling policies"],
        "cm": ["Committing API keys or database passwords to public GitHub repositories", "Disabling antivirus or firewalls to 'make code run faster'", "Copy-pasting proprietary company codebase into public consumer AI chatbots"],
        "fu": ["Why is pasting proprietary source code into public free consumer chatbots a major enterprise security violation?", "What is the Principle of Least Privilege in access management?"]
    },
    {
        "q": "How do you approach learning from failure when a software feature you built is rejected by users or fails in production?",
        "sub": "Resilience & Growth",
        "d": "Beginner",
        "ans": "Interviewer is assessing: resilience, data-driven humility, and growth mindset. In software, features frequently fail to achieve expected user engagement or encounter unforeseen technical edge cases. Protocol: 1) Accept data objectively without personal resentment or defensiveness, 2) Gather quantitative data (analytics, drop-off funnels, error logs) and qualitative feedback (user interviews) to understand WHY it failed, 3) Conduct a blameless post-mortem with the team to identify root assumptions that were incorrect, and 4) Iterate quickly: apply the lessons to redesign the feature or cleanly deprecate it to avoid maintenance overhead. Illustrative example (replace with your experience): 'When users ignored our advanced search filter in our project, I didn\\'t defend it. Analytics showed users preferred a single smart search bar. We simplified the interface based on data, and search engagement tripled. It taught me to fall in love with the user problem, not my specific solution.'",
        "kp": ["Separate personal self-worth from feature adoption", "Use quantitative telemetry and user feedback to diagnose failure root causes", "Conduct blameless post-mortems focused on system processes, not individuals", "Iterate fast or cleanly remove failed features to prevent code clutter"],
        "cm": ["Blaming users for 'not being smart enough to understand my feature'", "Refusing to remove or change a failed feature out of stubborn pride", "Giving up and losing motivation when work doesn't succeed on the first try"],
        "fu": ["What does the phrase 'Fall in love with the problem, not your solution' mean in engineering?", "How do feature flags allow teams to safely test and roll back experimental features?"]
    },
    {
        "q": "What is the importance of code readability vs code brevity? What is 'clever code'?",
        "sub": "Clean Code Philosophy",
        "d": "Beginner",
        "ans": "Interviewer is assessing: clean code philosophy and team engineering empathy. Programs are read 10 times more often than they are written. 'Clever code' refers to overly compressed, convoluted one-liners, obscure bitwise hacks, or deeply nested lambda chains that save 2 lines of code at the expense of hours of confusion for teammates. Professional code prioritizes clarity, explicit naming, clear flow, and maintainability over brevity. As Python's Zen states: 'Readability counts' and 'Explicit is better than implicit'. A clear 6-line function with descriptive variables is vastly superior to an unreadable 1-line comprehension. Illustrative example (replace with your code standard): 'In our project, I refactored a dense nested ternary list comprehension into a simple 5-line for-loop with clear helper functions. It made the code instantly understandable to my peers during code review and eliminated an off-by-one bug that was hidden in the clever one-liner.'",
        "kp": ["Code is read far more often than written; prioritize reader comprehension", "Avoid 'clever' convoluted one-liners that obscure business logic", "Explicit, descriptive variable and function names over obscure abbreviations", "'Explicit is better than implicit; Readability counts' (The Zen of Python)"],
        "cm": ["Writing 150-character complex list comprehensions with nested ternaries to look 'smart'", "Using single-letter variable names (like a, b, x, temp) throughout business logic", "Sacrificing clarity for negligible micro-optimizations that don't impact runtime"],
        "fu": ["When is a one-line list comprehension appropriate versus when should it be a for-loop?", "How do linters and static analysis tools enforce team readability standards?"]
    },
    {
        "q": "How would you handle a situation where a teammate is taking all the credit for a project you built together?",
        "sub": "Credit & Professionalism",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: professional assertiveness, composure, and navigating workplace credit. Getting emotional or creating a public scene damages your reputation. Protocol: 1) Stay calm and address privately: speak with the teammate 1-on-1 first ('I noticed during the presentation that my contributions to the database architecture and auth API weren\\'t mentioned. In future updates, I\\'d appreciate accurate representation of our shared work'), 2) Document your work: maintain clear written records of your deliverables via Git commit histories, pull request reviews, and documented task tickets (Jira/Trello), and 3) Let technical depth speak: in technical reviews and Q&A sessions, speak confidently and deeply about the specific modules you built. Senior leaders quickly recognize who wrote the code based on technical depth. Illustrative example (replace with your experience): 'When a teammate presented our group project and focused primarily on his parts, I spoke with him privately afterwards to align on fair representation. During the technical Q&A, I answered in-depth architectural questions about the backend modules I designed, clearly demonstrating my ownership to the evaluators without creating drama.'",
        "kp": ["Address privately with the peer first before escalating", "Rely on Git commit logs, PRs, and task tickets as objective proof of work", "Demonstrate undeniable ownership through technical depth during discussions", "Maintain professional composure; avoid public accusations"],
        "cm": ["Starting a public argument or screaming match in front of managers or clients", "Remaining completely silent and suffering in passive-aggressive resentment", "Sabotaging the project or refusing to collaborate further"],
        "fu": ["How do version control (Git blame) and issue trackers make credit stealing difficult in engineering?", "What role does a team lead play in ensuring fair credit distribution among team members?"]
    },
    {
        "q": "Why is punctuality, meeting discipline, and professional etiquette critical in a software engineering career?",
        "sub": "Professional Etiquette",
        "d": "Beginner",
        "ans": "Interviewer is assessing: basic professional discipline, reliability, and respect for colleagues' time. In global engineering teams spanning multiple timezones, punctuality is the foundation of professional trust: 1) Meeting Discipline: joining calls 2 minutes early, testing audio/video beforehand, coming prepared with an agenda, and staying focused (no multitasking or typing loudly while unmuted), 2) Asynchronous Discipline: responding to Slack/email messages within expected team SLAs, updating Jira ticket statuses accurately, and notifying leads proactively if you will be late or absent, and 3) Respect for Focus: keeping meetings short and on-topic so colleagues can return to deep coding blocks. Punctuality signals reliability and respect. Illustrative example (replace with your habits): 'I make it a rule to join project calls two minutes early with my audio tested. During presentations, I keep my camera on, stay fully engaged, and follow up with concise meeting notes, ensuring we respect everyone\\'s engineering time.'",
        "kp": ["Punctuality builds foundational professional trust and credibility", "Meeting etiquette: test audio/video early, stay engaged, avoid multitasking", "Respect teammates' deep-work coding blocks by keeping meetings concise", "Proactive communication if delays or absences occur"],
        "cm": ["Joining team meetings 10 minutes late regularly with audio issues", "Typing loudly on keyboard or multitasking while others are speaking on calls", "Disappearing for hours during work-from-home without updating team status"],
        "fu": ["What is asynchronous communication and why do remote-first engineering teams favor it over meetings?", "How does being reliably punctual accelerate leadership trust for freshers?"]
    }
]

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    f1 = OUT_DIR / "01.json"
    f2 = OUT_DIR / "02.json"
    f1.write_text(json.dumps(PART1, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    f2.write_text(json.dumps(PART2, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(PART1)} to 01.json, {len(PART2)} to 02.json (Total: {len(PART1) + len(PART2)})")

if __name__ == "__main__":
    main()
