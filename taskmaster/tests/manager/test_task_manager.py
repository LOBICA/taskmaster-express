from taskmaster.database.managers import TaskManager


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


async def test_set_main_priority_task(
    test_admin_user, task_factory, task_manager: TaskManager
):
    new_tasks = task_factory(test_admin_user, n=3)

    tasks = []
    for new_task in new_tasks:
        task = await task_manager.save(new_task)
        tasks.append(task)

    task = tasks[0]
    task.is_main_priority = True
    task = await task_manager.save(task)

    task = await task_manager.get(task.uuid)
    assert task.is_main_priority

    other_task = tasks[2]
    await task_manager.set_main_priority_for_date(other_task, task.due_date)

    task = await task_manager.get(task.uuid)
    assert not task.is_main_priority

    other_task = await task_manager.get(other_task.uuid)
    assert other_task.is_main_priority
