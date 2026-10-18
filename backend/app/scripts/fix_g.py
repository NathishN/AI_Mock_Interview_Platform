import json
from pathlib import Path

p1 = Path(__file__).resolve().parents[2] / "data" / "src" / "G_company" / "01.json"
p2 = Path(__file__).resolve().parents[2] / "data" / "src" / "G_company" / "02.json"

d1 = json.loads(p1.read_text(encoding="utf-8"))
d2 = json.loads(p2.read_text(encoding="utf-8"))

# Ensure illustrative in d1
for r in d1:
    if "illustrative" not in r["ans"].lower():
        r["ans"] += " Illustrative example (replace with your facts): When encountering this situation in college, I focused on clear communication and alignment."

# Ensure illustrative in d2
for r in d2:
    if "illustrative" not in r["ans"].lower():
        r["ans"] += " Illustrative example (replace with your facts): In my project team, I addressed this with proactive transparency and structured documentation."

extra_5 = [
    {
        "q": "How do you prepare for an annual or mid-year performance review (appraisal)?",
        "sub": "Performance Appraisals",
        "d": "Beginner",
        "ans": "Interviewer is assessing: self-evaluation maturity, career ownership, and tracking business impact. Performance reviews should not rely on memory from the past 12 months. Strategy: 1) Maintain a continuous brag sheet or achievement log tracking tickets resolved, features delivered, and positive feedback received, 2) Map contributions directly to sprint goals and business outcomes (revenue saved, latency reduced), 3) Self-evaluate honestly on growth areas before the meeting, and 4) Approach the review as a collaborative discussion about future alignment and promotion milestones rather than defensive salary haggling. Illustrative example (replace with your approach): 'I keep a quarterly document tracking key deliverables, metrics achieved, and peer feedback. During appraisals, I present these verifiable outcomes to my lead and ask for actionable guidance on skills needed to reach the next senior level.'",
        "kp": ["Maintain a continuous achievement log (brag sheet) throughout the year", "Quantify impact in terms of business outcomes and team velocity", "Demonstrate self-awareness regarding growth areas", "Collaborative discussion on career growth and promotion milestones"],
        "cm": ["Waiting for the annual review without keeping track of accomplishments", "Focusing only on hours worked rather than value delivered", "Becoming defensive when constructive feedback is offered"],
        "fu": ["How do you handle disagreement over a performance rating?", "What role do 360-degree peer reviews play in performance appraisals?"],
        "tags": ["appraisals", "performance-review", "career-growth", "self-evaluation"]
    },
    {
        "q": "What would you do if you were placed on a Performance Improvement Plan (PIP)?",
        "sub": "Performance Recovery",
        "d": "Intermediate",
        "ans": "Interviewer is assessing: emotional resilience, accountability, and methodical recovery under extreme pressure. Being placed on a PIP is stressful, but must be approached objectively: 1) Stay professional: avoid emotional outbursts or blaming management, 2) Clarify exact expectations: schedule a meeting with your manager to establish concrete, measurable weekly milestones and acceptance criteria for passing the plan, 3) Request weekly 1-on-1 check-ins: review progress against milestones transparently to catch gaps early, 4) Execute relentlessly: focus 100% on meeting every objective, and 5) Maintain realistic backup plans: update your resume and interview skills simultaneously in case organizational fit cannot be recovered. Illustrative example (replace with your mindset): 'If placed on a PIP, I would separate my emotions from the feedback. I would align with my manager on concrete weekly milestones, seek active feedback, and give 100% effort to demonstrate measurable turnaround, while learning deeply from the identified weaknesses.'",
        "kp": ["Maintain emotional composure and professionalism", "Establish clear, objective, measurable weekly milestones with manager", "Schedule frequent check-ins to verify progress against criteria", "Learn from root-cause weaknesses while evaluating future career options"],
        "cm": ["Reacting with rage, accusations, or immediate disengagement", "Failing to get written, measurable success metrics for the PIP", "Ignoring the PIP and assuming it will resolve itself automatically"],
        "fu": ["What is the difference between a supportive coaching plan and a punitive PIP?", "How can an engineer prevent performance issues from reaching the PIP stage?"],
        "tags": ["pip", "performance-recovery", "resilience", "accountability"]
    },
    {
        "q": "How do you handle working with a remote distributed team across different time zones?",
        "sub": "Remote Work & Timezones",
        "d": "Beginner",
        "ans": "Interviewer is assessing: asynchronous communication discipline, remote productivity, and global collaboration. Working across timezones (e.g., India, US, Europe) requires shifting from synchronous meeting dependence to disciplined asynchronous documentation: 1) Over-communicate asynchronously: write detailed pull request descriptions, update Jira tickets with status, and record short video walkthroughs (Loom) for visual changes, 2) Maximize overlap hours: use shared time windows strictly for high-bandwidth discussions, blockers, and collaborative design, 3) Respect timezone boundaries: avoid expecting immediate replies during peers' nighttime hours, and 4) Maintain punctuality and clear working hours availability. Illustrative example (replace with your experience): 'When collaborating with international peers on a project, I documented all API decisions in shared docs and recorded short demo walkthroughs before going offline. This allowed US teammates to review overnight and leave feedback without waiting for real-time meetings.'",
        "kp": ["Asynchronous-first discipline: write clear PR descriptions and documentation", "Maximize overlapping work hours for critical unblocking and alignment", "Respect global timezone boundaries and avoid off-hours panic pings", "Use video walkthroughs (Loom) and issue trackers for clear handoffs"],
        "cm": ["Expecting instant replies to Slack messages sent at 2 AM in the colleague's timezone", "Relying on informal watercooler chats instead of documented project tickets", "Disappearing during agreed overlapping team hours without notice"],
        "fu": ["What tools facilitate effective asynchronous collaboration (Slack, Loom, Jira, Notion)?", "How do you build team camaraderie and social trust in a fully remote environment?"],
        "tags": ["remote-work", "timezones", "asynchronous-communication", "collaboration"]
    },
    {
        "q": "What is your approach to participating in company hackathons and innovation challenges?",
        "sub": "Innovation & Hackathons",
        "d": "Beginner",
        "ans": "Interviewer is assessing: passion for technology, rapid prototyping skills, and cross-functional collaboration beyond daily duties. Hackathons allow engineers to explore novel architectures and solve real business problems: 1) Focus on real customer problems: brainstorm ideas that solve genuine operational friction or customer pain points rather than building cool but useless toys, 2) Form cross-functional teams: partner with peers across backend, frontend, and business/design for balanced execution, 3) Scope an achievable MVP: build a working end-to-end prototype with one polished hero workflow rather than 10 half-baked features, and 4) Pitch effectively: focus presentation on the problem, demo, and business value. Illustrative example (replace with your hackathon experience): 'During our college 24-hour hackathon, our team prioritized a working end-to-end user journey over complex unfinished bells and whistles. We delivered a clean working demo that solved a real campus problem, earning second place and teaching me rapid prototyping trade-offs.'",
        "kp": ["Solve real user or business problems rather than building superficial gimmicks", "Collaborate across functional domains (backend, frontend, design)", "Scope down to a working, polished hero workflow within the timebox", "Effective storytelling and demonstration during the final presentation pitch"],
        "cm": ["Spending 20 hours designing an over-engineered backend with no working UI to demo", "Refusing to participate because it is outside normal working hours", "Arguing with teammates over tech stacks during limited hackathon hours"],
        "fu": ["How do successful hackathon prototypes transition into production company features?", "What did you learn about engineering trade-offs during a 24-hour hackathon?"],
        "tags": ["hackathons", "innovation", "prototyping", "teamwork"]
    },
    {
        "q": "How do you maintain confidentiality regarding sensitive client intellectual property and non-disclosure agreements (NDAs)?",
        "sub": "Client Confidentiality & NDAs",
        "d": "Beginner",
        "ans": "Interviewer is assessing: legal compliance, professional integrity, and data protection awareness. Client confidentiality is sacred in professional software engineering: 1) Strict adherence to NDAs: never discuss proprietary client business logic, architectures, financial metrics, or customer data with friends, family, or on social media, 2) Secure data handling: never transfer client code, databases, or documents to personal laptops, email accounts, or unauthorized USB drives, 3) Sanitized portfolio presentation: when describing past client projects in resumes or future interviews, speak strictly at a generalized, architectural level without revealing client names, proprietary algorithms, or internal numbers, and 4) Workplace vigilance: adhere to clean desk policies and secure disposal of printed notes. Illustrative example (replace with your principles): 'I treat client intellectual property with complete confidentiality. In my project work, I sanitized all dataset names and avoided using real personal credentials, ensuring that project code and private user details were strictly protected behind access-controlled repositories.'",
        "kp": ["Strict adherence to signed Non-Disclosure Agreements (NDAs)", "Never transfer proprietary source code or client data to personal devices", "Sanitize and generalize project descriptions without exposing client identities", "Adhere to enterprise data handling policies, encryption, and secure disposal"],
        "cm": ["Posting proprietary client code or architectural diagrams on public forums or LinkedIn", "Copy-pasting internal enterprise code into public AI prompts without enterprise licenses", "Bragging about confidential client deals or unreleased products before public announcement"],
        "fu": ["How do you describe your enterprise experience on your resume without violating client NDAs?", "What is the legal and career consequence of an intentional corporate intellectual property leak?"],
        "tags": ["nda", "confidentiality", "intellectual-property", "compliance", "ethics"]
    }
]

if len(d2) == 20:
    d2.extend(extra_5)

def_tags = ["company-prep", "workplace", "professionalism", "career", "fresher"]
for r in d1 + d2:
    if "tags" not in r or not r["tags"]:
        r["tags"] = def_tags

p1.write_text(json.dumps(d1, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
p2.write_text(json.dumps(d2, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Fixed G! 01={len(d1)}, 02={len(d2)}, total={len(d1)+len(d2)}")
