import logging
from typing import Annotated

from fastapi import Depends
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from sqlalchemy import select

from taskmasterexp.auth.dependencies import CurrentUserWS
from taskmasterexp.database.dependencies import TaskManager
from taskmasterexp.database.models import TaskModel

from .client import chat_model

logger = logging.getLogger(__name__)

template = "You are a helpful assistant"
human_template = "{text}"


async def get_chat_prompt(
    user: CurrentUserWS, task_manager: TaskManager
) -> ChatPromptTemplate:
    logger.info(f"Getting chat prompt for user {user.uuid}")
    tasks = await task_manager.list({"user_id": user.uuid})

    tasks_details = ",".join(
        [f"{task.title} - {task.description or 'no description'}" for task in tasks]
    )

    messages = [
        ("system", template),
        ("system", "You are helping the user to organize their tasks"),
        ("system", "The task format is: [title] - [description]"),
        ("system", f"Here are the tasks you have to help with: [{tasks_details}]"),
        MessagesPlaceholder(variable_name="history"),
        ("human", human_template),
    ]

    logger.info(f"Chat prompt: {messages}")

    chat_prompt = ChatPromptTemplate.from_messages(messages)

    chain = chat_prompt | chat_model

    return chain


ChatPrompt = Annotated[ChatPromptTemplate, Depends(get_chat_prompt)]
