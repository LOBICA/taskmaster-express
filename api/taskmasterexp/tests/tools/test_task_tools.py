from uuid import UUID

from taskmasterexp.chatbot.tools import (
    add_new_task,
    complete_task,
    delete_task,
    get_task_list,
    modify_task,
)
from taskmasterexp.database.managers import TaskManager
from taskmasterexp.schemas.tasks import TaskStatus


async def test_task_list_tool(
    patch_task_manager, task_manager: TaskManager, task_factory, test_admin_user
):
    with patch_task_manager:
        task_list = await get_task_list.ainvoke({"user_id": str(test_admin_user.uuid)})
        assert task_list == ""

    task, *_ = task_factory(test_admin_user)
    task = await task_manager.save(task)

    with patch_task_manager:
        task_list = await get_task_list.ainvoke({"user_id": str(test_admin_user.uuid)})
        assert task_list == task.ai_format()


async def test_add_new_task_tool(
    patch_task_manager, task_manager: TaskManager, test_admin_user
):
    title = "New task"
    description = "this is a new task"

    with patch_task_manager:
        task_details: str = await add_new_task.ainvoke(
            {
                "user_id": str(test_admin_user.uuid),
                "title": title,
                "description": description,
            }
        )
        task_id, *_ = task_details.split(" | ")

    task = await task_manager.get(UUID(task_id))
    assert task.title == title
    assert task.description == description
    assert task.ai_format() == task_details


async def test_modify_task_tool(
    patch_task_manager, task_manager: TaskManager, task_factory, test_admin_user
):
    task, *_ = task_factory(test_admin_user)
    task = await task_manager.save(task)

    new_title = "Modified task"
    new_description = "this task has been modified"

    with patch_task_manager:
        task_details = await modify_task.ainvoke(
            {
                "task_id": str(task.uuid),
                "title": new_title,
                "description": new_description,
            }
        )

    task = await task_manager.get(task.uuid)
    assert task.title == new_title
    assert task.description == new_description
    assert task.ai_format() == task_details


async def test_complete_task_tool(
    patch_task_manager, task_manager: TaskManager, task_factory, test_admin_user
):
    task, *_ = task_factory(test_admin_user)
    task = await task_manager.save(task)

    with patch_task_manager:
        task_details = await complete_task.ainvoke({"task_id": str(task.uuid)})

    task = await task_manager.get(task.uuid)
    assert task.status == TaskStatus.DONE
    assert task.ai_format() == task_details


async def test_delete_task_tool(
    patch_task_manager, task_manager: TaskManager, task_factory, test_admin_user
):
    task, *_ = task_factory(test_admin_user)
    task = await task_manager.save(task)

    with patch_task_manager:
        await delete_task.ainvoke({"task_id": str(task.uuid)})

    task = await task_manager.get(task.uuid)
    assert task is None
