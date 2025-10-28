from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.task import router as task_router
from app.db.session import engine, verify_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure the database is reachable before serving requests
    verify_connection(engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(task_router)
