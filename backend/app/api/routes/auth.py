from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.api.deps import CurrentUser, DbDep
from app.core.security import (
    DUMMY_HASH,
    TokenError,
    create_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models import User, UserProfile
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenPair,
    UserOut,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def _tokens(user: User) -> TokenPair:
    return TokenPair(
        access_token=create_token(user.id, "access"),
        refresh_token=create_token(user.id, "refresh"),
    )


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, db: DbDep) -> AuthResponse:
    if db.scalar(select(User.id).where(User.email == body.email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "An account with this email already exists")
    user = User(
        email=body.email,
        password_hash=hash_password(body.password),
        full_name=body.full_name,
        last_login_at=datetime.now(timezone.utc),
    )
    user.profile = UserProfile()
    db.add(user)
    try:
        db.commit()
    except IntegrityError:  # concurrent registration with the same email
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "An account with this email already exists")
    return AuthResponse(user=UserOut.model_validate(user), tokens=_tokens(user))


@router.post("/login", response_model=AuthResponse)
def login(body: LoginRequest, db: DbDep) -> AuthResponse:
    user = db.scalar(select(User).where(User.email == body.email))
    # Always run one bcrypt check so response time doesn't reveal account existence.
    ok = verify_password(body.password, user.password_hash if user else DUMMY_HASH)
    if user is None or not ok or not user.is_active:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user.last_login_at = datetime.now(timezone.utc)
    db.commit()
    return AuthResponse(user=UserOut.model_validate(user), tokens=_tokens(user))


@router.post("/refresh", response_model=TokenPair)
def refresh(body: RefreshRequest, db: DbDep) -> TokenPair:
    try:
        user_id = decode_token(body.refresh_token, "refresh")
    except TokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired refresh token")
    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired refresh token")
    return _tokens(user)


@router.post("/reset-password", response_model=dict)
def reset_password(body: ResetPasswordRequest, db: DbDep) -> dict:
    user = db.scalar(select(User).where(User.email == body.email))
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No account found with this email address")
    user.password_hash = hash_password(body.new_password)
    db.commit()
    return {"message": "Password updated successfully. You can now sign in with your new password."}


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser) -> User:
    return user
