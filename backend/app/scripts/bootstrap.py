"""Idempotent first-run setup: default rubrics + optional admin account.

    python -m app.scripts.bootstrap

Existing rubrics are never overwritten, so admin edits survive redeploys.
"""

import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models import Rubric, User, UserProfile
from app.models.enums import UserRole
from app.schemas.rubric import RubricIn
from app.services.rubrics import DEFAULT_RUBRICS

log = logging.getLogger("bootstrap")


def seed_rubrics(db: Session) -> int:
    created = 0
    for key, spec in DEFAULT_RUBRICS.items():
        RubricIn.model_validate(spec)  # fails loudly if weights don't sum to 100
        if db.get(Rubric, key) is None:
            db.add(Rubric(key=key, name=spec["name"], dimensions=spec["dimensions"]))
            created += 1
    db.commit()
    return created


def ensure_admin(db: Session) -> bool:
    s = get_settings()
    email = s.bootstrap_admin_email.strip().lower()
    if not email or not s.bootstrap_admin_password:
        return False
    if db.scalar(select(User.id).where(User.email == email)):
        return False
    user = User(
        email=email,
        password_hash=hash_password(s.bootstrap_admin_password),
        full_name="Administrator",
        role=UserRole.ADMIN.value,
    )
    user.profile = UserProfile()
    db.add(user)
    db.commit()
    return True


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    with SessionLocal() as db:
        log.info("rubrics created: %d", seed_rubrics(db))
        log.info("admin created: %s", ensure_admin(db))


if __name__ == "__main__":
    main()
