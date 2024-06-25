from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from taskmasterexp.settings import PSQL_CONNECTION_STRING


@asynccontextmanager
async def get_engine() -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(PSQL_CONNECTION_STRING)
    yield engine
    await engine.dispose()


@asynccontextmanager
async def get_session(engine) -> AsyncGenerator[AsyncSession]:
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
