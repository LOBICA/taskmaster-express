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
    title: str = ""
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    due_date: date | None = None
    mood: TaskMood = TaskMood.NEUTRAL


class Task(TaskData):
    uuid: UUID | None = None

    def update(self, data: dict):
        self.title = data.get('title', self.title)
        self.description = data.get('description', self.description)
        self.status = data.get('status', self.status)
        self.due_date = data.get('due_date', self.due_date)
        self.mood = data.get('mood', self.mood)

    class Config:
        orm_mode = True


class TaskResponse(TaskData):
    uuid: UUID
