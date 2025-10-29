# Task Tracker Backend

Tech stack
- FastAPI + Uvicorn
- SQLModel
- Alembic
- PostgreSQL (psycopg driver)
- Pydantic v2
- Docker

Run locally
1) Prereqs: Python 3.12+, PostgreSQL running
2) launch postgres
   - `docker compose -f ../docker/db/docker-compose.yml up -d`
3) activate virtual env
   - `python -m venv .venv`
   - `source .venv/bin/activate`
4) Install deps: `pip install -r requirements.txt`
5) Set env:
   - Linux/macOS: `export DATABASE_URL=postgresql+psycopg://task_tracker:task_tracker@localhost:5432/task_tracker`
6) Apply migrations: `alembic upgrade head` (or: `./apply_migrations.sh`)
7) Start API (dev): `uvicorn app.main:app --reload`
8) Open docs: http://localhost:8000/docs

Run with Docker (single container)
1) Build image: `docker build -t task-tracker-backend .`
2) `docker compose -f ../docker/prod/docker-compose.yml up -d`

Useful files
- test.http — sample API requests (use REST Client or curl)
