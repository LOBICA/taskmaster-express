from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import managers
from .connection import get_engine, get_session
from .redis import get_redis, redis


async def inject_db_session():
    async with get_engine() as engine:
        async with get_session(engine) as session:
            yield session


DBSession = Annotated[AsyncSession, Depends(inject_db_session)]


async def inject_task_manager(session: DBSession):
    return managers.TaskManager(session)


TaskManager = Annotated[managers.TaskManager, Depends(inject_task_manager)]


async def inject_user_manager(session: DBSession):
    return managers.UserManager(session)


UserManager = Annotated[managers.UserManager, Depends(inject_user_manager)]


async def inject_subscriptions_manager(session: DBSession):
    return managers.SubscriptionManager(session)


SubscriptionManager = Annotated[
    managers.SubscriptionManager, Depends(inject_subscriptions_manager)
]


async def inject_redis():
    async with get_redis() as conn:
        yield conn


Redis = Annotated[redis.Redis, Depends(inject_redis)]
