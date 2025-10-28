from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, Response
from sqlmodel import Session

from app.db.session import engine
from app.schemas.task import TaskDto, IdResponseDto, TaskCreateDto, TaskUpdateDto
from app.enums.status import StatusEnum
from app.crud.task import create_task as crud_create_task, list_tasks as crud_list_tasks, update_task as crud_update_task, delete_task as crud_delete_task
from app.utils.mapper import to_task_dto

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=IdResponseDto)
async def create_task(payload: TaskCreateDto):
    with Session(engine) as session:
        task = crud_create_task(session, title=payload.title, description=payload.description, status=payload.status)
        return IdResponseDto(id=task.id)


@router.get("", response_model=List[TaskDto])
async def list_tasks(status: Optional[StatusEnum] = Query(None, description="Filter by status")):
    with Session(engine) as session:
        rows = crud_list_tasks(session, status=status)
        return [to_task_dto(t) for t in rows]


@router.patch("/{task_id}", response_model=TaskDto)
async def update_task(task_id: int, payload: TaskUpdateDto):
    with Session(engine) as session:
        update_data = payload.model_dump(exclude_unset=True)
        task = crud_update_task(session, task_id, **update_data)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return to_task_dto(task)


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int):
    with Session(engine) as session:
        ok = crud_delete_task(session, task_id)
        if not ok:
            # As before, returning 204 even if not found, but FastAPI will still send 204
            raise HTTPException(status_code=204, detail="Task not found")
        return Response(status_code=204)
