# launch dev database in docker/db

export DATABASE_URL=postgresql+psycopg://task_tracker:task_tracker@localhost:5432/task_tracker
alembic upgrade head
