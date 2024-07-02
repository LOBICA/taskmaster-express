from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Self
from uuid import UUID

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from taskmasterexp.database.connection import get_engine, get_session
from taskmasterexp.schemas.tasks import Task
from taskmasterexp.schemas.users import User

from .models import TaskModel, UserModel


class BaseManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    @classmethod
    @asynccontextmanager
    async def start_session(cls) -> AsyncGenerator[Self, Any]:
        async with get_engine() as engine:
            async with get_session(engine) as session:
                yield cls(session)


class UserManager(BaseManager):
    async def list(self) -> list[User]:
        stmt = select(UserModel)
        result: Result = await self.session.execute(stmt)
        return [User.from_orm(model) for model in result.scalars()]

    async def get(self, user_id: UUID) -> User | None:
        model = await self.session.get(UserModel, user_id)
        if model:
            return User.from_orm(model)

        return None

    async def get_by_phone(self, phone_number: str) -> User | None:
        stmt = select(UserModel).where(UserModel.phone_number == phone_number)
        result: Result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            return User.from_orm(model)

        return None

    async def save(self, user: User, password: str = None) -> User:
        if user.uuid:
            model = await self.session.get(UserModel, user.uuid)
            for field, value in user.dict().items():
                setattr(model, field, value)
        else:
            model = UserModel(**user.dict(exclude={"uuid"}))
            self.session.add(model)

        if password:
            model.set_password(password)

        await self.session.commit()
        await self.session.refresh(model)
        return User.from_orm(model)

    async def change_password(
        self, user_id: UUID, password: str, new_password: str
    ) -> None:
        model = await self.session.get(UserModel, user_id)
        if model:
            if model.verify_password(password):
                model.set_password(new_password)
                await self.session.commit()
            else:
                raise ValueError("Invalid password")

    async def delete(self, user_id: UUID) -> None:
        model = await self.session.get(UserModel, user_id)
        if model:
            await self.session.delete(model)
            await self.session.commit()


class TaskManager(BaseManager):
    async def list(self, params: dict = None) -> list[Task]:
        stmt = select(TaskModel)
        if params:
            if "user_id" in params:
                stmt = stmt.where(TaskModel.user_id == params["user_id"])
            if "status" in params:
                stmt = stmt.where(TaskModel.status == params["status"])
        result: Result = await self.session.execute(stmt)
        return [Task.from_orm(model) for model in result.scalars()]

    async def get(self, task_id: UUID) -> Task | None:
        model = await self.session.get(TaskModel, task_id)
        if model:
            return Task.from_orm(model)

        return None

    async def save(self, task: Task) -> Task:
        if task.uuid:
            model = await self.session.get(TaskModel, task.uuid)
            for field, value in task.dict().items():
                setattr(model, field, value)
        else:
            model = TaskModel(**task.dict(exclude={"uuid"}))
            self.session.add(model)

        await self.session.commit()
        await self.session.refresh(model)
        return Task.from_orm(model)

    async def delete(self, task_id: UUID) -> None:
        model = await self.session.get(TaskModel, task_id)
        if model:
            await self.session.delete(model)
            await self.session.commit()
