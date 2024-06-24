import logging
from typing import Annotated

from fastapi import Depends
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder

from taskmasterexp.auth.dependencies import CurrentUserWS

from .client import chat_model
from .tools import tools

logger = logging.getLogger(__name__)

template = "You are a helpful assistant"
human_template = "{text}"


async def get_chat_agent(
    user: CurrentUserWS,
) -> AgentExecutor:
    logger.info(f"Getting chat prompt for user {user.uuid}")

    task_data = "[uuid] | [title] | [description] | [status] | [due_date] | [mood]"

    task_template = "[title]: [description]"

    messages = [
        ("system", "You are a helpful assistant"),
        ("system", "You are helping the user to organize their tasks"),
        ("system", f"The user's uuid is {user.uuid}"),
        ("human", f"My name is {user.name}"),
        ("system", f"The task format is: <{task_data}>"),
        ("system", "You will list the tasks as: <\n1.[title]\n2.[title]\n...>"),
        ("system", "If the task list is empty you will say that there are no tasks"),
        (
            "system",
            f"When giving more details about a tasks you will present them as {task_template}.",
        ),
        ("system", "Greet back the user, only provide task information if asked"),
        ("system", "Always reference the updated list of tasks"),
        MessagesPlaceholder(variable_name="history"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
        ("human", human_template),
    ]

    chat_prompt = ChatPromptTemplate.from_messages(messages)

    agent = create_openai_tools_agent(chat_model, tools, chat_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor


ChatAgent = Annotated[AgentExecutor, Depends(get_chat_agent)]
