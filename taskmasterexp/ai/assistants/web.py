import logging

from langchain.agents import AgentExecutor
from redis import Redis

from taskmasterexp.schemas.users import User

from ..checkpoint.redis import AsyncRedisSaver
from .chat_agent import get_chat_agent

logger = logging.getLogger(__name__)


async def get_web_chat_agent(
    user: User,
    redis: Redis,
) -> AgentExecutor:
    return await get_chat_agent(user, AsyncRedisSaver(redis))
