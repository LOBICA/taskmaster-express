import logging
from typing import Annotated

from fastapi import Depends
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder

from taskmasterexp.auth.dependencies import CurrentUserWS

from .client import chat_model

logger = logging.getLogger(__name__)

template = "You are a helpful assistant"
human_template = "{text}"


async def get_chat_prompt(
    user: CurrentUserWS,
) -> ChatPromptTemplate:
    logger.info(f"Getting chat prompt for user {user.uuid}")

    task_data = "[uuid] | [title] | [description] | [status] | [due_date] | [mood]"

    task_template = (
        "[title], [description], due for: [due_date if due_date else 'no due date']"
    )

    messages = [
        ("system", "You are a helpful assistant"),
        ("system", "You are helping the user to organize their tasks"),
        ("system", f"The user name is {user.name}"),
        ("system", f"The task format is: <{task_data}>"),
        ("system", "Here are the user's current tasks: [{tasks}]"),
        ("system", "You will list the tasks as: <\n1.[title]\n2.[title]\n...>"),
        (
            "system",
            f"When giving more details about a tasks you will present them as {task_template}.",
        ),
        ("system", "Greet back the user, only provide task information if asked"),
        ("system", "Always reference the updated list of tasks"),
        MessagesPlaceholder(variable_name="history"),
        ("human", human_template),
    ]

    logger.info(f"Chat prompt: {messages}")

    chat_prompt = ChatPromptTemplate.from_messages(messages)

    chain = chat_prompt | chat_model

    return chain


ChatPrompt = Annotated[ChatPromptTemplate, Depends(get_chat_prompt)]
