from datetime import date, datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from taskmasterexp.schemas.tasks import TaskMood, TaskStatus


class BaseModel(AsyncAttrs, DeclarativeBase):
    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())


class TaskModel(BaseModel):
    __tablename__ = "tasks"

    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[TaskStatus]
    due_date: Mapped[Optional[date]]
    mood: Mapped[TaskMood]
