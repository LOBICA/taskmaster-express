import json
from datetime import date
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from taskmaster.encoder import CustomEncoder


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
    is_main_priority: bool = False

    def update(self, data: dict):
        self.title = data.get("title", self.title)
        self.description = data.get("description", self.description)
        self.status = data.get("status", self.status)
        self.due_date = data.get("due_date", self.due_date)
        self.mood = data.get("mood", self.mood)
        self.is_main_priority = data.get("is_main_priority", self.is_main_priority)


class Task(TaskData):
    uuid: UUID | None = None
    user_id: UUID

    def to_json(self):
        return json.dumps(self.model_dump(), cls=CustomEncoder)

    @staticmethod
    def ai_format_template():
        return " | ".join(
            [
                "[uuid]",
                "[title]",
                "[description]",
                "[status]",
                "[due_date]",
                "[mood]",
                "[is_main_priority]",
            ]
        )

    def ai_format(self):
        return " | ".join(
            [
                str(self.uuid),
                self.title,
                self.description,
                str(self.status.value),
                str(self.due_date),
                str(self.mood.value),
                str(self.is_main_priority),
            ]
        )

    model_config = ConfigDict(from_attributes=True)


class TaskResponse(TaskData):
    uuid: UUID
