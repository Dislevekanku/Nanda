"""Database session management."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

try:
    engine = create_engine(settings.database_url, pool_pre_ping=True)
except ModuleNotFoundError:  # pragma: no cover - fallback for environments without drivers
    engine = create_engine("sqlite:///./medspa.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
