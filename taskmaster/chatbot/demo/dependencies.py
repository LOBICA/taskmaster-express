from typing import Annotated

from fastapi import Depends
from langchain.agents import AgentExecutor

from taskmaster.auth.dependencies import CurrentUser

from . import assistant


async def _get_demo_chat_agent(user: CurrentUser):
    return await assistant.get_demo_chat_agent(user)


DemoAgent = Annotated[AgentExecutor, Depends(_get_demo_chat_agent)]
