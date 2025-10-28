from typing import Optional, List

from fastapi import FastAPI, HTTPException, Query, Response
from sqlmodel import Session, select

from model.dto import TaskDto, IdResponseDto, TaskCreateDto, TaskUpdateDto
from models import Task as DbTask, StatusEnum
from db import engine

app = FastAPI()

def _to_api_task(db_task: DbTask) -> TaskDto:
    return TaskDto(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        status=db_task.status,
    )

@app.post("/tasks", response_model=IdResponseDto)
async def create_task(payload: TaskCreateDto):
    with Session(engine) as session:
        db_task = DbTask(title=payload.title, description=payload.description, status=payload.status)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return IdResponseDto(id=db_task.id)  # type: ignore[arg-type]


@app.get("/tasks", response_model=List[TaskDto])
async def list_tasks(status: Optional[StatusEnum] = Query(None, description="Filter by status")):
    with Session(engine) as session:
        stmt = select(DbTask)
        if status is not None:
            stmt = stmt.where(DbTask.status == status)
        rows = session.exec(stmt).all()
        return [_to_api_task(t) for t in rows]


@app.patch("/tasks/{task_id}", response_model=TaskDto)
async def update_task(task_id: int, payload: TaskUpdateDto):
    with Session(engine) as session:
        db_task = session.get(DbTask, task_id)
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return _to_api_task(db_task)


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    with Session(engine) as session:
        db_task = session.get(DbTask, task_id)
        if db_task is None:
            raise HTTPException(status_code=204, detail="Task not found")
        session.delete(db_task)
        session.commit()
        return Response(status_code=204)
