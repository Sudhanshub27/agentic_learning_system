"""
Agentic Learning System - Database Engine & Session Factory

Async SQLAlchemy setup that works with both SQLite (dev) and PostgreSQL (prod).
Uses the async engine pattern for non-blocking database operations.
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


# Create async engine from DATABASE_URL in settings
# echo=True in dev for SQL query logging, False in production
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    # SQLite needs this for async support
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)

# Session factory — creates new async sessions for each request
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    All models inherit from this to get automatic table creation.
    """
    pass


async def get_db() -> AsyncSession:
    """
    Dependency injection for FastAPI routes.
    Yields a database session and ensures cleanup.

    Usage in routes:
        @router.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Create all database tables on startup.
    In production, use Alembic migrations instead.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Cleanup database connections on shutdown."""
    await engine.dispose()
