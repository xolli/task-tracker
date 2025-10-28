import os
from sqlmodel import create_engine

# DATABASE_URL is the single source of truth
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
