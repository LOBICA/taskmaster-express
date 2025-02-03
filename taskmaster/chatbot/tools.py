import datetime
import logging
from uuid import UUID

from langchain_core.tools import tool

from taskmaster.database.managers import TaskManager, UserManager
from taskmaster.schemas.tasks import Task, TaskStatus

logger = logging.getLogger(__name__)


@tool
async def get_pending_task_list(user_id: str) -> str | None:
    """Return the user's pending task list.

    This tool doen't return the task for an specific date like "today",
    if you need tasks for a specific date, use get_tasks_for_date.

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
    """Return the user's tasks for a date provided in isoformat.

    Provided the user's uuid and the date, return the list of tasks for that user
    on that date, or None if there was an error.

    Always tell back the user the date that you used to get the tasks. If there
    is a task that is the main priority list it at the beginning and let the user now.
    """
    logger.info(f"Getting tasks for user {user_id} on date {date}")
    async with TaskManager.start_session() as manager:
        try:
            tasks = await manager.list(
                {
                    "user_id": UUID(user_id),
                    "due_date": datetime.datetime.fromisoformat(date).date(),
                }
            )
            tasks_details = ",".join([task.ai_format() for task in tasks])
        except Exception:
            logger.exception(f"Error getting tasks for user {user_id} on date {date}")
            return None
        logger.info(tasks_details)

    return tasks_details


@tool
async def add_new_task(
    user_id: str,
    title: str,
    description: str,
    due_date: str = None,
    is_main_priority: bool = False,
) -> str | None:
    """Add a new task for the user.

    Provided the user's uuid, the task title, and the task description.

    Add a due_date if the user has provided it. Also, mark the task as
    the main priority if the user has requested it.

    Returns the newly created task details, or None if there was an error.
    """
    logger.info(f"Adding new task for user {user_id}")
    async with TaskManager.start_session() as manager:
        try:
            if due_date:
                due_date = datetime.datetime.fromisoformat(due_date).date()

            task = Task(
                user_id=UUID(user_id),
                title=title,
                description=description,
                due_date=due_date,
            )
            task = await manager.save(task)

            if task.due_date and is_main_priority:
                await manager.set_main_priority_for_date(task, task.due_date)
        except Exception:
            logger.exception(f"Error adding new task for user {user_id}")
            return None

    return task.ai_format()


@tool
async def modify_task(task_id: str, title: str, description: str) -> str | None:
    """Change a task title and description

    Provided the task's uuid, the new title, and the new description.

    If you are required to change the task's due date, use set_task_due_date.

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
async def set_task_due_date(task_id: str, due_date: str) -> str | None:
    """Set or change the due date for a task.

    Provided the task's uuid and the new due date in isoformat.

    Returns the updated task details, or None if there was an error.
    """
    logger.info(f"Setting due date {due_date} for task {task_id}")
    async with TaskManager.start_session() as manager:
        try:
            task = await manager.get(UUID(task_id))
            task.due_date = datetime.datetime.fromisoformat(due_date).date()
            task = await manager.save(task)
        except Exception:
            logger.exception(f"Error setting due date for task {task_id}")
            return None

    return task.ai_format()


@tool
def set_main_priority(main_priority: str, date: str):
    """Set the main priority for the date."""
    instructions = (
        f"Check if the user has a pending task for {main_priority}. "
        f"If it does, set that task as the main priority for {date}."
        f"If it doesn't, create a new task with title [{main_priority}] with "
        f"the [due date] '{date}', [is_main_priority] as true, "
        f"and an appropiate [description]."
    )
    return instructions


@tool
async def set_task_as_main_priority_for_date(task_id: str, date: str) -> str | None:
    """Set a task as the main priority for a specific date.

    Provided the task's uuid and the date in isoformat.

    Returns the updated task details, or None if there was an error.
    """
    logger.info(f"Setting main priority for task {task_id} on date {date}")
    async with TaskManager.start_session() as manager:
        try:
            task = await manager.get(UUID(task_id))
            await manager.set_main_priority_for_date(
                task, datetime.datetime.fromisoformat(date).date()
            )
        except Exception:
            logger.exception(
                f"Error setting main priority for task {task_id} on date {date}"
            )
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
    set_main_priority,
    get_pending_task_list,
    get_tasks_for_date,
    add_new_task,
    modify_task,
    set_task_due_date,
    set_task_as_main_priority_for_date,
    complete_task,
    delete_task,
    associate_email_to_user,
]
