import logging

from langchain.agents import AgentExecutor
from redis import Redis

from taskmaster.schemas.users import User
from taskmaster.settings import DEMO_PHONE_NUMBERS

from ..checkpoint.redis import AsyncRedisSaver
from ..demo import get_demo_chat_agent
from .chat_agent import get_chat_agent

logger = logging.getLogger(__name__)


async def get_whatsapp_chat_agent(
    user: User,
    redis: Redis,
) -> AgentExecutor:
    if user.phone_number in DEMO_PHONE_NUMBERS:
        return await get_demo_chat_agent(user)
    return await get_chat_agent(user, AsyncRedisSaver(redis))
