"""Async SQLAlchemy engine + session factory for pal-web.

Matches the existing project convention: single AsyncSession per request,
declarative Base shared by all models.
"""

from __future__ import annotations

import os
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = os.environ.get(
    "PALWEB_DATABASE_URL",
    "postgresql+asyncpg://palweb:palweb@localhost:5432/palweb",
)


class Base(DeclarativeBase):
    """Declarative base for all pal-web ORM models."""


engine = create_async_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency yielding one AsyncSession per request."""
    async with SessionLocal() as session:
        yield session
