from typing import Annotated

from fastapi import Depends
from langchain.agents import AgentExecutor

from taskmasterexp.auth.dependencies import CurrentUserWA, CurrentUserWS
from taskmasterexp.database.dependencies import Redis

from . import twilio
from .assistants.web import get_web_chat_agent
from .assistants.whatsapp import get_whatsapp_chat_agent


async def inject_web_chat_agent(user: CurrentUserWS, redis: Redis) -> AgentExecutor:
    return await get_web_chat_agent(user, redis)


ChatAgent = Annotated[AgentExecutor, Depends(inject_web_chat_agent)]


async def inject_whatsapp_chat_agent(
    user: CurrentUserWA, redis: Redis
) -> AgentExecutor:
    return await get_whatsapp_chat_agent(user, redis)


WhatsAppAgent = Annotated[AgentExecutor, Depends(inject_whatsapp_chat_agent)]


async def inject_twilio_client() -> twilio.Client:
    return twilio.get_twilio_client()


TwilioClient = Annotated[twilio.Client, Depends(inject_twilio_client)]
