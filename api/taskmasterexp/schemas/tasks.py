from datetime import date
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class TaskStatus(str, Enum):
    PENDING = "pending"
    DONE = "done"


class TaskMood(Enum):
    VERY_STRESSED = "very stressed"
    STRESSED = "stressed"
    UNCONFORTABLE = "unconfortable"
    NEUTRAL = "neutral"
    GOOD = "good"
    EXCITED = "exited"
    VERY_EXCITED = "very excited"


class TaskData(BaseModel):
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    due_date: date | None = None
    mood: TaskMood = TaskMood.NEUTRAL


class Task(TaskData):
    uuid: UUID

    def update(self, new_version: TaskData):
        self.title = new_version.title
        self.description = new_version.description
        self.status = new_version.status
        self.due_date = new_version.due_date
        self.mood = new_version.mood

    class Config:
        orm_mode = True


class TaskResponse(TaskData):
    uuid: UUID
