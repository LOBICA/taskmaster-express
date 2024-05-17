from uuid import UUID

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from taskmasterexp.database.dependencies import TaskManager
from taskmasterexp.schemas.tasks import Task, TaskData, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskResponse])
async def list_tasks(manager: TaskManager):
    tasks = await manager.list()
    return tasks


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
async def add_tasks(data: TaskData, manager: TaskManager):
    task = Task(**data.dict())
    task = await manager.save(task)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID, manager: TaskManager):
    task = await manager.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def modify_task(task_id: UUID, data: TaskData, manager: TaskManager):
    task = await manager.get(task_id)

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    task.update(data.dict(exclude_unset=True))
    await manager.save(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID, manager: TaskManager):
    await manager.delete(task_id)
