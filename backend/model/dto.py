from typing import Optional, List
from pydantic import BaseModel, Field

from models import StatusEnum


class TaskCreateDto(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.pending


class TaskUpdateDto(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    status: Optional[StatusEnum] = None


class TaskDto(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: StatusEnum


class IdResponseDto(BaseModel):
    id: int
