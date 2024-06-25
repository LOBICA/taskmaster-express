from unittest.mock import patch

from taskmasterexp.chatbot.tools import get_task_list
from taskmasterexp.database.managers import TaskManager


async def test_task_list_tool(
    task_manager_generator, db_session, task_factory, test_admin_user
):
    with patch(
        "taskmasterexp.chatbot.tools.TaskManager.start_session", task_manager_generator
    ):
        task_list = await get_task_list.ainvoke(str(test_admin_user.uuid))
        assert task_list == ""

    manager = TaskManager(db_session)
    task, *_ = task_factory(test_admin_user)
    task = await manager.save(task)

    with patch(
        "taskmasterexp.chatbot.tools.TaskManager.start_session", task_manager_generator
    ):
        task_list = await get_task_list.ainvoke(str(test_admin_user.uuid))
        assert task_list == task.ai_format()
