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

    name: Mapped[str]
    email: Mapped[str | None] = mapped_column(unique=True)
    password: Mapped[str | None]

    phone_number: Mapped[str | None] = mapped_column(unique=True)

    fb_user_id: Mapped[str | None]
    fb_access_token: Mapped[str | None]

    tasks: Mapped[list["TaskModel"]] = relationship(
        back_populates="user", cascade="all, delete"
    )

    disabled: Mapped[bool] = mapped_column(default=False)

    def set_password(self, password: str):
        self.password = pwd_context.hash(password)

    def verify_password(self, password: str):
        if self.password is None:
            return False

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
