from uuid import uuid4


async def test_list_tasks(
    test_admin_client, test_admin_user, task_factory, task_manager
):
    response = test_admin_client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

    task_count = 5
    tasks = task_factory(test_admin_user, task_count)
    for task in tasks:
        await task_manager.save(task)

    response = test_admin_client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == task_count


async def test_add_task(test_admin_client, test_admin_user, task_factory):
    response = test_admin_client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

    task, *_ = task_factory(test_admin_user)
    response = test_admin_client.post("/tasks", content=task.to_json())
    assert response.status_code == 201
    task_response = response.json()
    assert task_response["title"] == task.title

    response = test_admin_client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1


async def test_get_task(test_admin_client, test_admin_user, task_factory, task_manager):
    uuid = uuid4()
    response = test_admin_client.get(f"/tasks/{uuid}")
    assert response.status_code == 404

    task_data, *_ = task_factory(test_admin_user)
    task = await task_manager.save(task_data)

    response = test_admin_client.get(f"/tasks/{task.uuid}")
    assert response.status_code == 200
    task_response = response.json()
    assert task_response["title"] == task.title


async def test_patch_task(
    test_admin_client, test_admin_user, task_factory, task_manager
):
    task_data, *_ = task_factory(test_admin_user)

    uuid = uuid4()
    response = test_admin_client.patch(f"/tasks/{uuid}", content=task_data.to_json())
    assert response.status_code == 404

    task = await task_manager.save(task_data)

    task_data.title = "updated title"
    response = test_admin_client.patch(
        f"/tasks/{task.uuid}", content=task_data.to_json()
    )
    assert response.status_code == 200
    task_response = response.json()
    assert task_response["title"] == task_data.title

    task = await task_manager.get(task.uuid)
    assert task.title == "updated title"


async def test_delete_task(
    test_admin_client, test_admin_user, task_factory, task_manager
):
    task_data, *_ = task_factory(test_admin_user)
    task = await task_manager.save(task_data)

    response = test_admin_client.delete(f"/tasks/{task.uuid}")
    assert response.status_code == 204

    task = await task_manager.get(task.uuid)
    assert task is None
