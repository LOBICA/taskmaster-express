import logging

from sqlalchemy import text

from .connection import get_engine, get_session

logger = logging.getLogger(__name__)


async def ping() -> bool:
    try:
        async with get_engine() as engine:
            async with get_session(engine) as session:
                result = await session.execute(text("SELECT 1"))
                return result.scalar() == 1
    except Exception:
        logger.exception("Database connection failed")
        return False
