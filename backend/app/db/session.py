import os
from typing import Optional
from urllib.parse import quote_plus

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import create_engine


def _resolve_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if url:
        # Normalize to psycopg driver if scheme is generic postgresql://
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url
    raise RuntimeError(
        "Database connection is not configured. Set DATABASE_URL"
        "Examples: DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/mydb"
    )


DATABASE_URL = _resolve_database_url()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def verify_connection(db_engine=None) -> None:
    """Verify database connectivity at startup"""
    eng = db_engine or engine
    try:
        with eng.connect() as conn:
            conn.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise RuntimeError(
            f"Failed to connect to the database using URL '{DATABASE_URL}'. "
            f"Cause: {exc.__class__.__name__}: {exc}. "
        ) from exc
