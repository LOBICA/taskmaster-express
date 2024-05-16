from uuid import UUID

from fastapi import APIRouter

from taskmasterexp.database.dependencies import TaskManager
from taskmasterexp.schemas.tasks import TaskData, TaskResponse, Task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskResponse])
async def list_tasks(manager: TaskManager):
    tasks = await manager.list()
    return tasks


@router.post("/", status_code=201, response_model=TaskResponse)
async def add_tasks(data: TaskData, manager: TaskManager):
    task = Task(**data.dict())
    task = await manager.save(task)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID, manager: TaskManager):
    task = await manager.get(task_id)
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def modify_task(task_id: UUID, data: TaskData, manager: TaskManager):
    task = await manager.get(task_id)

    task.update(data.dict(exclude_unset=True))
    await manager.save(task)

    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: UUID, manager: TaskManager):
    await manager.delete(task_id)
