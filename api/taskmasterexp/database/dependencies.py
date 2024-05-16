from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import managers
from .connection import get_engine, get_session


async def inject_db_session():
    async with get_engine() as engine:
        async with get_session(engine) as session:
            yield session


DBSession = Annotated[AsyncSession, Depends(inject_db_session)]


async def inject_task_manager(session: DBSession):
    return managers.TaskManager(session)


TaskManager = Annotated[managers.TaskManager, Depends(inject_task_manager)]
