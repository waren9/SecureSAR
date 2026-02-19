from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.utils.config import load_config


cfg = load_config()
engine = create_engine(cfg.db.postgres_dsn, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency-style generator for FastAPI if you later want DB access.
    Not currently used in the demo endpoints (pipeline is file-based),
    but included for completeness.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


