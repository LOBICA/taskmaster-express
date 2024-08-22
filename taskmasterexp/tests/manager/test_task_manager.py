from taskmasterexp.database.managers import TaskManager


async def test_task_manager(test_admin_user, task_factory, task_manager: TaskManager):
    tasks = await task_manager.list()
    assert tasks == []

    new_task, *_ = task_factory(test_admin_user)
    task = await task_manager.save(new_task)
    assert task.title == new_task.title

    tasks = await task_manager.list()
    assert tasks == [task]

    task_ = await task_manager.get(task.uuid)
    assert task == task_

    task_.title = "update title"
    task = await task_manager.save(task_)
    assert task.title == "update title"

    await task_manager.delete(task.uuid)
    tasks = await task_manager.list()
    assert tasks == []
    task_ = await task_manager.get(task.uuid)
    assert task_ is None
