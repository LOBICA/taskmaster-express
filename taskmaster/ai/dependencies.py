"""Define the dependencies injected into the FastAPI endpoints."""
from typing import Annotated

from fastapi import Depends
from langchain.agents import AgentExecutor

from taskmaster.auth.dependencies import CurrentUserWA, CurrentUserWS
from taskmaster.database.dependencies import Redis

from .assistants.web import get_web_chat_agent
from .assistants.whatsapp import get_whatsapp_chat_agent


# ChatAgent dependency
async def inject_web_chat_agent(user: CurrentUserWS, redis: Redis) -> AgentExecutor:
    return await get_web_chat_agent(user, redis)


ChatAgent = Annotated[AgentExecutor, Depends(inject_web_chat_agent)]


# WhatsAppAgent dependency
async def inject_whatsapp_chat_agent(
    user: CurrentUserWA, redis: Redis
) -> AgentExecutor:
    return await get_whatsapp_chat_agent(user, redis)


WhatsAppAgent = Annotated[AgentExecutor, Depends(inject_whatsapp_chat_agent)]
