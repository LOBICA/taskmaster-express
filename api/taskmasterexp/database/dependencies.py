from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import managers
from .connection import get_session

DBSession = Annotated[AsyncSession, Depends(get_session)]


async def inject_task_manager(session: DBSession):
    return managers.TaskManager(session)


TaskManager = Annotated[managers.TaskManager, Depends(inject_task_manager)]
