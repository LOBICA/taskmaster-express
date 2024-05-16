from uuid import UUID

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from taskmasterexp.schemas.tasks import Task

from .models import TaskModel


class TaskManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self, params: dict = None) -> list[Task]:
        stmt = select(TaskModel)
        result: Result = await self.session.execute(stmt)
        return [Task.from_orm(model) for model in result.scalars()]

    async def get(self, task_id: UUID) -> Task:
        model = await self.session.get(TaskModel, task_id)
        return Task.from_orm(model)

    async def save(self, task: Task) -> None:
        model = await self.session.get(TaskModel, task.uuid)
        if model:
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
