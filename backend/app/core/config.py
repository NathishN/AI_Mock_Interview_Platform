from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_INSECURE_SECRETS = {"", "change-me", "change-me-to-a-long-random-string"}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "InterviewAce AI"
    environment: str = "development"  # development | test | production
    api_prefix: str = "/api/v1"

    database_url: str = (
        "postgresql+psycopg://interviewace:interviewace@localhost:5432/interviewace"
    )

    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14

    # Comma-separated list of allowed browser origins.
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # Optional first admin, created by `python -m app.scripts.bootstrap`.
    bootstrap_admin_email: str = ""
    bootstrap_admin_password: str = ""

    # Used from phase 3 onwards. Server-side only; never sent to the frontend.
    groq_api_key: str = ""
    groq_model: str = "qwen/qwen3.8-27b"
    groq_timeout_seconds: float = 30.0
    groq_max_retries: int = 2

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @model_validator(mode="after")
    def _check_production_secrets(self) -> "Settings":
        if self.is_production:
            if self.jwt_secret_key in _INSECURE_SECRETS or len(self.jwt_secret_key) < 32:
                raise ValueError(
                    "JWT_SECRET_KEY must be set to a random value of at least 32 characters in production."
                )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
