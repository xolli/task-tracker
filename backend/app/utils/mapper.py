from app.models.task import Task
from app.schemas.task import TaskDto


def to_task_dto(task: Task) -> TaskDto:
    return TaskDto(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )
