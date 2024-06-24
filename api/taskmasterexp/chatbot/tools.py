import logging
from datetime import datetime
from uuid import UUID

from langchain_core.tools import tool

from taskmasterexp.database.connection import get_engine, get_session
from taskmasterexp.database.managers import TaskManager

logger = logging.getLogger(__name__)


@tool
def get_current_time() -> str:
    """Return the current time in ISO format."""
    return datetime.now().isoformat()


@tool()
async def get_task_list(user_id: str) -> str:
    """Return the user's task list.

    Provided the user's uuid, return the list of tasks for that user.
    """
    logger.info(f"Getting task list for user {user_id}")
    async with get_engine() as engine:
        async with get_session(engine) as session:
            manager = TaskManager(session)
            tasks = await manager.list({"user_id": UUID(user_id)})
            tasks_details = ",".join(
                [
                    f"{task.uuid} | {task.title} | {task.description} | {task.status} | {task.due_date} | {task.mood}"
                    for task in tasks
                ]
            )
            logger.info(tasks_details)

    return tasks_details


tools = [
    get_current_time,
    get_task_list,
]
