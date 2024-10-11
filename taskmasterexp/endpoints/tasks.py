import datetime
from uuid import UUID

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from taskmasterexp.auth import CurrentUser
from taskmasterexp.database.dependencies import TaskManager
from taskmasterexp.schemas.tasks import Task, TaskData, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    current_user: CurrentUser,
    manager: TaskManager,
    status: str = None,
    date: datetime.date = None,
):
    filter = {
        "user_id": current_user.uuid,
    }

    if status:
        filter["status"] = status

    if date:
        filter["due_date"] = date

    tasks = await manager.list(filter)
    return tasks


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
async def add_tasks(current_user: CurrentUser, manager: TaskManager, data: TaskData):
    task = Task(user_id=current_user.uuid, **data.model_dump())
    task = await manager.save(task)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(current_user: CurrentUser, manager: TaskManager, task_id: UUID):
    task = await manager.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if task.user_id != current_user.uuid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def modify_task(
    current_user: CurrentUser, manager: TaskManager, task_id: UUID, data: TaskData
):
    task = await manager.get(task_id)

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if task.user_id != current_user.uuid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    task.update(data.model_dump(exclude_unset=True))
    await manager.save(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(current_user: CurrentUser, manager: TaskManager, task_id: UUID):
    task = await manager.get(task_id)

    if task:
        if task.user_id != current_user.uuid:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        await manager.delete(task_id)
