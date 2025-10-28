from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field

from app.enums.status import StatusEnum


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=1)
    description: Optional[str] = None
    status: StatusEnum = Field(default=StatusEnum.pending, index=True)
    created_at: Optional[datetime] = Field(default=None, nullable=True)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)
