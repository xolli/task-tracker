from typing import List, Optional

from sqlmodel import Session, select

from app.models.task import Task
from app.enums.status import StatusEnum


def create_task(session: Session, title: str, description: Optional[str], status: StatusEnum) -> Task:
    task = Task(title=title, description=description, status=status)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def list_tasks(session: Session, status: Optional[StatusEnum] = None) -> List[Task]:
    stmt = select(Task)
    if status is not None:
        stmt = stmt.where(Task.status == status)
    return list(session.exec(stmt).all())


def update_task(session: Session, task_id: int, **update_fields) -> Optional[Task]:
    task = session.get(Task, task_id)
    if task is None:
        return None
    for key, value in update_fields.items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: int) -> bool:
    task = session.get(Task, task_id)
    if task is None:
        return False
    session.delete(task)
    session.commit()
    return True
