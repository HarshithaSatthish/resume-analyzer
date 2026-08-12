from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.config import settings
from app.database import close_mongodb_connection, connect_to_mongodb, ensure_indexes
from app.middleware.error_handler import register_exception_handlers


@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_to_mongodb()
    await ensure_indexes()
    yield
    await close_mongodb_connection()


app = FastAPI(
    title=settings.app_name,
    description="Production-ready AI Resume Analyzer API with ATS scoring, skill extraction, and Gemini insights.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(api_router, prefix="/api")


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "AI Resume Analyzer API",
        "docs": "/docs",
        "health": "/api/health",
    }
