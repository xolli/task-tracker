from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.enums.status import StatusEnum


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
    created_at: datetime
    updated_at: Optional[datetime] = None


class IdResponseDto(BaseModel):
    id: int