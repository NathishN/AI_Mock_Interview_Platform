"""Knowledge-base tooling: expand authoring files, validate, report.

Authoring layout (backend/data/src/<dir>/):
  _defaults.json  -> id_prefix, category, target, default roles/stages/criteria
  NN.json         -> list of compact records (q, sub, d, ans, kp, cm, fu, tags,
                     optional roles/stages/crit/type/rubric overrides)
Records get IDs <prefix>-001, -002, ... in file order, so ONLY APPEND; never
reorder or delete (sessions reference IDs). Retire a question via the admin API.
"""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import ValidationError

from app.schemas.question import QuestionCreate

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
SRC_DIR = DATA_DIR / "src"
SEED_FILE = DATA_DIR / "questions_seed.json"

TOTAL_TARGET = 500
EXPECTED_TARGETS = {
    "HR": 100, "Behavioral": 60, "Resume & Projects": 60, "Python": 60,
    "SQL & Analytics": 50, "ML, AI & GenAI": 60, "Company & Workplace": 50, "Coding": 60,
}
PERSONAL_CATEGORIES = {"HR", "Behavioral", "Resume & Projects", "Company & Workplace"}
MARKER = "illustrative"  # personal-answer examples must be labelled as such
_STOP = set("a an the of to in on for and or is are do does did you your we our us me my i what why how would should can could with this that it be have has about at as by from".split())


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)
    targets: dict[str, int] = field(default_factory=dict)

    @property
    def total(self) -> int:
        return sum(self.counts.values())


def expand_source(src_dir: Path = SRC_DIR) -> tuple[list[dict], dict[str, int]]:
    """Returns (full records, {category: target}). Skips directories with no data files."""
    records: list[dict] = []
    targets: dict[str, int] = dict(EXPECTED_TARGETS)
    for cat_dir in sorted(p for p in src_dir.iterdir() if p.is_dir()):
        files = sorted(f for f in cat_dir.glob("*.json") if not f.name.startswith("_"))
        defaults_path = cat_dir / "_defaults.json"
        if not defaults_path.exists():
            continue
        d = json.loads(defaults_path.read_text(encoding="utf-8"))
        targets[d["category"]] = d["target"]
        n = 0
        for f in files:
            for r in json.loads(f.read_text(encoding="utf-8")):
                n += 1
                rec = {
                    "id": f"{d['id_prefix']}-{n:03d}",
                    "question": r["q"],
                    "category": d["category"],
                    "subcategory": r["sub"],
                    "difficulty": r["d"],
                    "target_roles": r.get("roles", d["roles"]),
                    "interview_stage": r.get("stages", d["stages"]),
                    "reference_answer": r["ans"],
                    "key_points": r["kp"],
                    "evaluation_criteria": r.get("crit", d["criteria"]),
                    "common_mistakes": r["cm"],
                    "follow_up_questions": r["fu"],
                    "tags": r["tags"],
                }
                if "type" in r:
                    rec["question_type"] = r["type"]
                if "rubric" in r:
                    rec["rubric_key"] = r["rubric"]
                records.append(rec)
    return records, targets


def _tokens(text: str) -> frozenset[str]:
    return frozenset(w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in _STOP)


def validate_records(records: list[dict], targets: dict[str, int] | None = None, strict: bool = False) -> Report:
    rep = Report(targets=targets or {})
    ids: set[str] = set()
    parsed: list[tuple[str, frozenset[str]]] = []
    for i, raw in enumerate(records):
        rid = raw.get("id", f"#{i}")
        try:
            q = QuestionCreate.model_validate(raw)
        except ValidationError as exc:
            for e in exc.errors():
                rep.errors.append(f"{rid}: {'.'.join(map(str, e['loc']))}: {e['msg']}")
            continue
        if q.id in ids:
            rep.errors.append(f"{q.id}: duplicate id")
        ids.add(q.id)
        cat = q.category.value
        rep.counts[cat] = rep.counts.get(cat, 0) + 1
        if len(q.key_points) < 3:
            rep.warnings.append(f"{q.id}: fewer than 3 key_points")
        if len(q.reference_answer) < 200 and q.category.value != "Coding":
            rep.warnings.append(f"{q.id}: reference_answer under 200 chars")
        if cat in PERSONAL_CATEGORIES and MARKER not in q.reference_answer.lower():
            rep.warnings.append(f"{q.id}: no clearly labelled illustrative example")
        parsed.append((q.id, _tokens(q.question)))

    # Near-duplicate questions (token-set Jaccard), across all categories.
    for a in range(len(parsed)):
        for b in range(a + 1, len(parsed)):
            ta, tb = parsed[a][1], parsed[b][1]
            if ta and tb and len(ta & tb) / len(ta | tb) >= 0.7:
                rep.errors.append(f"{parsed[a][0]} ~ {parsed[b][0]}: near-duplicate questions")

    for cat, target in (targets or {}).items():
        got = rep.counts.get(cat, 0)
        if got > target or (strict and got != target):
            rep.errors.append(f"category '{cat}': {got} questions, expected {target}")
    if strict and len(ids) != TOTAL_TARGET:
        rep.errors.append(f"total: {len(ids)} questions, expected exactly {TOTAL_TARGET}")
    return rep


def format_report(rep: Report) -> str:
    lines = ["Category progress:"]
    for cat, target in rep.targets.items():
        got = rep.counts.get(cat, 0)
        lines.append(f"  {cat:<22} {got:>3} / {target}")
    lines.append(f"  {'TOTAL':<22} {rep.total:>3} / {TOTAL_TARGET}")
    lines.append(f"Errors: {len(rep.errors)}   Warnings: {len(rep.warnings)}")
    lines += [f"  ERROR   {e}" for e in rep.errors[:50]]
    lines += [f"  warning {w}" for w in rep.warnings[:50]]
    return "\n".join(lines)


def load_seed(path: Path = SEED_FILE) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["questions"]
