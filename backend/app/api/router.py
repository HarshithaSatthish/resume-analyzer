from fastapi import APIRouter

from app.api import ai, analyze, ats, auth, compare, parse, reports, upload
from app.config import settings
from app.database.health import get_database_health
from app.schemas.common import DatabaseHealth, HealthResponse

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(upload.router)
api_router.include_router(parse.router)
api_router.include_router(ats.router)
api_router.include_router(ai.router)
api_router.include_router(analyze.router)
api_router.include_router(compare.router)
api_router.include_router(reports.router)


@api_router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    db_health = await get_database_health()
    overall_status = "healthy" if db_health.get("connected") else "degraded"

    return HealthResponse(
        status=overall_status,
        app_name=settings.app_name,
        environment=settings.app_env,
        database=DatabaseHealth(**db_health),
    )
