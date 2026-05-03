"""
Agentic Learning System - FastAPI Application Entry Point

This is the main application that ties everything together:
- Database initialization on startup
- API route registration
- Health check endpoints
- LLM provider status
- CORS middleware for frontend (Phase 8)
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import init_db, close_db
from app.services.llm_service import llm_service

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Runs startup logic before the app serves requests,
    and cleanup logic when the app shuts down.
    """
    # === STARTUP ===
    logger.info("=" * 60)
    logger.info(f"🚀 Starting {settings.app_name}")
    logger.info(f"   Environment: {settings.app_env}")
    logger.info(f"   Debug: {settings.debug}")
    logger.info(f"   Database: {settings.database_url}")
    logger.info(f"   LLM Providers: {settings.available_providers}")
    logger.info("=" * 60)

    # Initialize database tables
    # Import models to register them with SQLAlchemy metadata
    import app.models  # noqa: F401
    await init_db()
    logger.info("✅ Database initialized")

    yield  # App is running and serving requests

    # === SHUTDOWN ===
    logger.info("🛑 Shutting down...")
    await close_db()
    logger.info("✅ Database connections closed")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description=(
        "An autonomous AI-powered learning system with multi-agent architecture. "
        "Uses 6 specialized agents (Planner, Tutor, Evaluator, Analyzer, Strategy, Memory) "
        "to create personalized learning experiences for ANY subject domain."
    ),
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc",    # ReDoc
)

# CORS middleware — allows frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "*", # Fallback
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# Health & Status Endpoints
# ============================================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint — confirms the API is running."""
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Detailed health check — reports status of all subsystems.
    Use this to verify database and LLM providers are working.
    """
    return {
        "status": "healthy",
        "environment": settings.app_env,
        "database": "connected",
        "llm_providers": settings.available_providers,
    }


@app.get("/health/llm", tags=["Health"])
async def llm_health():
    """
    Check LLM provider connectivity.
    Tests each configured provider with a minimal request.
    ⚠️ This endpoint is slow — it pings every provider.
    """
    results = await llm_service.health_check()
    all_healthy = all(v == "healthy" for v in results.values())
    return {
        "status": "all_healthy" if all_healthy else "degraded",
        "providers": results,
    }


# ============================================
# API Routes (will be added in Phase 7)
# ============================================
from app.api.routes_learning import router as learning_router
from app.api.routes_progress import router as progress_router

# app.include_router(user_router, prefix="/api/user", tags=["User"])
# app.include_router(session_router, prefix="/api/session", tags=["Session"])
app.include_router(progress_router, prefix="/api/progress", tags=["Progress"])
app.include_router(learning_router, prefix="/api/learning", tags=["Learning"])
