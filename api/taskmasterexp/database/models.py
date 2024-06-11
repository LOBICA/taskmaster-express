from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

from passlib.context import CryptContext
from sqlalchemy import ForeignKey, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from taskmasterexp.schemas.tasks import TaskMood, TaskStatus


class BaseModel(AsyncAttrs, DeclarativeBase):
    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(BaseModel):
    __tablename__ = "users"

    email: Mapped[str]
    password: Mapped[str]

    tasks: Mapped[list["TaskModel"]] = relationship(back_populates="user")

    def set_password(self, password: str):
        self.password = pwd_context.hash(password)

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password)


class TaskModel(BaseModel):
    __tablename__ = "tasks"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"))
    user: Mapped["UserModel"] = relationship(back_populates="tasks")

    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[TaskStatus]
    due_date: Mapped[Optional[date]]
    mood: Mapped[TaskMood]
