import pytest
from pydantic import ValidationError

from app.schemas.rubric import RubricIn
from app.services.rubrics import DEFAULT_RUBRICS
from tests.conftest import API


def test_default_rubric_weights_sum_to_100():
    for spec in DEFAULT_RUBRICS.values():
        RubricIn.model_validate(spec)
        assert sum(d["weight"] for d in spec["dimensions"]) == 100


def test_rubric_weights_must_sum_to_100():
    with pytest.raises(ValidationError):
        RubricIn(name="Bad", dimensions=[{"name": "A", "weight": 60}, {"name": "B", "weight": 30}])


def test_bootstrap_is_idempotent(db_session):
    from app.scripts.bootstrap import seed_rubrics
    assert seed_rubrics(db_session) == 0  # fixture already seeded them


def test_admin_can_edit_rubric_with_validation(client, admin_headers):
    ok = client.put(f"{API}/admin/rubrics/technical", headers=admin_headers, json={
        "name": "Technical v2",
        "dimensions": [{"name": "Correctness", "weight": 70}, {"name": "Clarity", "weight": 30}]})
    assert ok.status_code == 200 and ok.json()["name"] == "Technical v2"
    bad = client.put(f"{API}/admin/rubrics/technical", headers=admin_headers, json={
        "name": "Broken", "dimensions": [{"name": "Correctness", "weight": 70}]})
    assert bad.status_code == 422


def test_health_endpoints(client):
    assert client.get(f"{API}/health").json() == {"status": "ok"}
    assert client.get(f"{API}/health/ready").json() == {"status": "ready"}
