import logging
from datetime import datetime
from uuid import UUID

from langchain_core.tools import tool

from taskmasterexp.database.managers import TaskManager, UserManager
from taskmasterexp.schemas.tasks import Task, TaskStatus

logger = logging.getLogger(__name__)


@tool
def get_current_time() -> str:
    """Return the current time in ISO format."""
    return datetime.now().isoformat()


@tool
async def get_task_list(user_id: str) -> str | None:
    """Return the user's pending task list.

    Provided the user's uuid, return the list of tasks for that user,
    or None if there was an error.
    """
    logger.info(f"Getting task list for user {user_id}")
    async with TaskManager.start_session() as manager:
        try:
            tasks = await manager.list(
                {
                    "user_id": UUID(user_id),
                    "status": TaskStatus.PENDING,
                }
            )
            tasks_details = ",".join([task.ai_format() for task in tasks])
        except Exception:
            logger.exception(f"Error getting task list for user {user_id}")
            return None
        logger.info(tasks_details)

    return tasks_details


@tool
async def get_tasks_for_date(user_id: str, date: str) -> str | None:
    """Return the user's tasks for a specific date.

    Provided the user's uuid and the date, return the list of tasks for that user
    on that date, or None if there was an error.
    """
    logger.info(f"Getting tasks for user {user_id} on date {date}")
    async with TaskManager.start_session() as manager:
        try:
            tasks = await manager.list(
                {
                    "user_id": UUID(user_id),
                    "due_date": date,
                }
            )
            tasks_details = ",".join([task.ai_format() for task in tasks])
        except Exception:
            logger.exception(f"Error getting tasks for user {user_id} on date {date}")
            return None
        logger.info(tasks_details)

    return tasks_details


@tool
async def add_new_task(user_id: str, title: str, description: str) -> str | None:
    """Add a new task for the user.

    Provided the user's uuid, the task title, and the task description.

    Returns the newly created task details, or None if there was an error.
    """
    logger.info(f"Adding new task for user {user_id}")
    async with TaskManager.start_session() as manager:
        try:
            task = Task(user_id=UUID(user_id), title=title, description=description)
            task = await manager.save(task)
        except Exception:
            logger.exception(f"Error adding new task for user {user_id}")
            return None

    return task.ai_format()


@tool
async def modify_task(task_id: str, title: str, description: str) -> str | None:
    """Change a task title and description

    Provided the task's uuid, the new title, and the new description.

    Returns the updated task details, or None if there was an error.
    """
    logger.info(f"Modifying task {task_id}")
    async with TaskManager.start_session() as manager:
        try:
            task = await manager.get(UUID(task_id))
            task.title = title
            task.description = description
            task = await manager.save(task)
        except Exception:
            logger.exception(f"Error modifying task {task_id}")
            return None

    return task.ai_format()


@tool
async def complete_task(task_id: str) -> str | None:
    """Mark a task as done.

    Provided the task's uuid, mark the task as done.

    Returns the updated task details, or None if there was an error.
    """
    logger.info(f"Completing task {task_id}")
    async with TaskManager.start_session() as manager:
        try:
            task = await manager.get(UUID(task_id))
            task.status = TaskStatus.DONE
            await manager.save(task)
        except Exception:
            logger.exception(f"Error completing task {task_id}")
            return None

    return task.ai_format()


@tool
async def delete_task(task_id: str):
    """Delete a task.

    Provided the task's uuid, delete the task.

    Returns True if the task was deleted, otherwise False.
    """
    logger.info(f"Deleting task {task_id}")
    async with TaskManager.start_session() as manager:
        try:
            await manager.delete(UUID(task_id))
        except Exception:
            logger.exception(f"Error deleting task {task_id}")
            return False

        return True


@tool
async def associate_email_to_user(user_id: str, email: str):
    """Associate an email to a user.

    Provided the user's uuid and the email, associate the email to the user.

    If the email was associated correctly, return True, otherwise False.
    """
    email = email.lower()
    logger.info(f"Associating email {email} to user {user_id}")
    async with UserManager.start_session() as manager:
        try:
            await manager.associate_email(UUID(user_id), email)
        except Exception:
            logger.exception(f"Error associating email {email} to user {user_id}")
            return False

        return True


tools = [
    get_current_time,
    get_task_list,
    add_new_task,
    modify_task,
    complete_task,
    delete_task,
    associate_email_to_user,
]
