import logging
from typing import Annotated

from fastapi import Depends
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder

from taskmasterexp.auth.dependencies import CurrentUserWS
from taskmasterexp.schemas.tasks import Task

from .client import chat_model
from .tools import tools

logger = logging.getLogger(__name__)

template = "You are a helpful assistant"
human_template = "{text}"


async def get_chat_agent(
    user: CurrentUserWS,
) -> AgentExecutor:
    logger.info(f"Getting chat prompt for user {user.uuid}")

    task_template = "[title]\n[description]\nStatus: [status]\n"

    messages = [
        ("system", "You are a helpful assistant"),
        ("system", "You are helping the user to organize their tasks"),
        ("system", f"The user's uuid is {user.uuid}"),
        ("human", f"My name is {user.name}"),
        ("system", f"The task format is: <{Task.ai_format_template()}>"),
        ("system", "You will list the tasks as: <\n1.[title]\n2.[title]\n...>"),
        ("system", "If the task list is empty you will say that there are no tasks"),
        (
            "system",
            "When giving more details about a tasks "
            f"you will present them as {task_template}.",
        ),
        ("system", "Greet back the user, only provide task information if asked"),
        ("system", "Always reference the updated list of tasks"),
        ("system", "Only call the add_new_task tool once per chain"),
        MessagesPlaceholder(variable_name="history"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
        ("human", human_template),
    ]
    logger.info(messages)

    chat_prompt = ChatPromptTemplate.from_messages(messages)

    agent = create_openai_tools_agent(chat_model, tools, chat_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor


ChatAgent = Annotated[AgentExecutor, Depends(get_chat_agent)]
