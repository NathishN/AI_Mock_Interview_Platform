"""Knowledge-base CLI.

    python -m app.scripts.kb build            expand data/src -> data/questions_seed.json (validates first)
    python -m app.scripts.kb validate         validate the seed file  (--strict: exactly 500, all categories)
    python -m app.scripts.kb seed             insert missing questions into the database
    python -m app.scripts.kb seed --update    also overwrite questions that already exist
"""

import argparse
import json
import sys

from app.services.kb import (
    SEED_FILE, TOTAL_TARGET, expand_source, format_report, load_seed, validate_records,
)

DISCLAIMER = (
    "Curated collection of commonly encountered interview questions for Indian engineering "
    "freshers. Not a statistically ranked list of the most frequently asked questions."
)


def cmd_build(strict: bool) -> int:
    records, targets = expand_source()
    rep = validate_records(records, targets, strict=strict)
    print(format_report(rep))
    if rep.errors:
        print("\nNot written: fix errors first.")
        return 1
    SEED_FILE.write_text(
        json.dumps({"description": DISCLAIMER, "count": len(records), "questions": records},
                   indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nWrote {len(records)} questions to {SEED_FILE}")
    return 0


def cmd_validate(strict: bool) -> int:
    records = load_seed()
    _, targets = expand_source()
    rep = validate_records(records, targets, strict=strict)
    print(format_report(rep))
    return 1 if rep.errors else 0


def cmd_seed(update: bool, require_complete: bool) -> int:
    from app.db.session import SessionLocal
    from app.services.question_import import import_questions

    if not SEED_FILE.exists():
        print("No seed file found; nothing to seed.")
        return 0
    records = load_seed()
    if require_complete and len(records) != TOTAL_TARGET:
        print(f"Seed has {len(records)} questions, expected {TOTAL_TARGET}.")
        return 1
    with SessionLocal() as db:
        res = import_questions(db, records, update_existing=update)
    if not res.ok:
        for e in res.errors[:20]:
            print(f"  {e.id or e.index}: {'; '.join(e.errors)}")
        return 1
    print(f"Seed OK: created={res.created} updated={res.updated} skipped={res.skipped}")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("build", "validate"):
        sp = sub.add_parser(name)
        sp.add_argument("--strict", action="store_true")
    sp = sub.add_parser("seed")
    sp.add_argument("--update", action="store_true")
    sp.add_argument("--require-complete", action="store_true")
    a = ap.parse_args()
    code = {"build": lambda: cmd_build(a.strict), "validate": lambda: cmd_validate(a.strict),
            "seed": lambda: cmd_seed(a.update, a.require_complete)}[a.cmd]()
    sys.exit(code)


if __name__ == "__main__":
    main()
