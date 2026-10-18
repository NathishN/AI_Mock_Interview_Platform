from fastapi import APIRouter

from app.api.deps import CurrentUser, DbDep
from app.models import UserProfile
from app.schemas.profile import ProfileOut, ProfileUpdate

router = APIRouter(prefix="/profile", tags=["profile"])

_REQUIRED_FOR_ONBOARDING = ("degree", "branch", "graduation_year", "target_role")


def _out(user, profile: UserProfile) -> ProfileOut:
    out = ProfileOut.model_validate(profile)
    out.full_name = user.full_name
    return out


@router.get("/me", response_model=ProfileOut)
def get_profile(user: CurrentUser, db: DbDep) -> ProfileOut:
    if user.profile is None:
        user.profile = UserProfile()
        db.commit()
    return _out(user, user.profile)


@router.put("/me", response_model=ProfileOut)
def update_profile(body: ProfileUpdate, user: CurrentUser, db: DbDep) -> ProfileOut:
    profile = user.profile or UserProfile()
    user.profile = profile
    data = body.model_dump(exclude_unset=True)
    if "full_name" in data:
        name = data.pop("full_name")
        if name and name.strip():
            user.full_name = name.strip()
    for field, value in data.items():
        if field == "target_role" and value is not None:
            value = getattr(value, "value", value)
        setattr(profile, field, value)
    profile.onboarding_completed = all(
        getattr(profile, f) not in (None, "") for f in _REQUIRED_FOR_ONBOARDING
    )
    db.commit()
    return _out(user, profile)
