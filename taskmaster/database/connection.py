from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from taskmaster.settings import PSQL_CONNECTION_STRING


@asynccontextmanager
async def get_engine() -> AsyncGenerator[AsyncEngine, Any]:
    engine = create_async_engine(PSQL_CONNECTION_STRING)
    yield engine
    await engine.dispose()


@asynccontextmanager
async def get_session(engine) -> AsyncGenerator[AsyncSession, Any]:
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
