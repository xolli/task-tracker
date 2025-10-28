from fastapi import FastAPI

from app.api.task import router as task_router

app = FastAPI()

app.include_router(task_router)
