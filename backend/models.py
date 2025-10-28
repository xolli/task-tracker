from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


class StatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=1)
    description: Optional[str] = None
    status: StatusEnum = Field(default=StatusEnum.pending, index=True)
