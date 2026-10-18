import pytest
from sqlalchemy import func, select

from app.models import Question
from app.services.kb import EXPECTED_TARGETS, expand_source, load_seed, validate_records
from app.services.question_import import import_questions


def test_seed_file_matches_authoring_sources():
    records, _ = expand_source()
    assert load_seed() == records  # seed JSON is up to date; run `python -m app.scripts.kb build`


def test_seed_is_valid_and_has_no_errors_or_warnings():
    records = load_seed()
    rep = validate_records(records, dict(EXPECTED_TARGETS))
    assert rep.errors == []
    assert rep.warnings == []


def test_seeded_category_counts_never_exceed_targets_and_hr_is_complete():
    rep = validate_records(load_seed(), dict(EXPECTED_TARGETS))
    for cat, n in rep.counts.items():
        assert n <= EXPECTED_TARGETS[cat]
    assert rep.counts["HR"] == 100


def test_strict_mode_passes_at_exactly_500_and_fails_on_partial():
    seed = load_seed()
    # At exactly 500, strict mode passes without error
    rep_full = validate_records(seed, dict(EXPECTED_TARGETS), strict=True)
    assert rep_full.errors == []
    assert rep_full.total == 500

    # On a partial subset, strict mode flags the deficit
    rep_partial = validate_records(seed[:100], dict(EXPECTED_TARGETS), strict=True)
    assert any("expected exactly 500" in e for e in rep_partial.errors)


def test_ids_unique_and_no_empty_required_fields():
    records = load_seed()
    assert len({r["id"] for r in records}) == len(records)
    for r in records:
        for f in ("question", "reference_answer", "key_points", "evaluation_criteria", "target_roles"):
            assert r[f], (r["id"], f)


def test_validator_catches_near_duplicates_and_bad_records():
    base = dict(load_seed()[0])
    dup = dict(base, id="hr-900", question="Tell me about yourself?")
    bad = dict(base, id="hr-901", question="A different question about weekends?", key_points=[])
    rep = validate_records([base, dup, bad])
    assert any("near-duplicate" in e for e in rep.errors)
    assert any("hr-901" in e and "key_points" in e for e in rep.errors)


def test_seeding_inserts_missing_only_and_keeps_admin_edits(db_session):
    records = load_seed()
    first = import_questions(db_session, records, update_existing=False)
    assert first.ok and first.created == len(records)

    row = db_session.get(Question, "hr-001")
    row.difficulty = "Advanced"  # simulate an admin edit
    db_session.commit()

    again = import_questions(db_session, records, update_existing=False)
    assert again.created == 0 and again.skipped == len(records)
    assert db_session.get(Question, "hr-001").difficulty == "Advanced"
    assert db_session.scalar(select(func.count()).select_from(Question)) == len(records)
