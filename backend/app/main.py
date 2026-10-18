from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    admin,
    analytics,
    auth,
    company_prep,
    health,
    hr_studio,
    interviews,
    profile,
    questions,
    roadmap,
)
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        docs_url=None if settings.is_production else "/docs",
        redoc_url=None,
        openapi_url=None if settings.is_production else "/openapi.json",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=False,  # tokens travel in the Authorization header
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )
    prefix = settings.api_prefix
    for r in (
        health.router,
        auth.router,
        profile.router,
        questions.router,
        admin.router,
        interviews.router,
        hr_studio.router,
        analytics.router,
        company_prep.router,
        roadmap.router,
    ):
        app.include_router(r, prefix=prefix)
    return app


app = create_app()
