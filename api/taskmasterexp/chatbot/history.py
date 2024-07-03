import json

from pydantic import BaseModel

from taskmasterexp.auth.dependencies import CurrentUserWA
from taskmasterexp.database.dependencies import Redis


class Message(BaseModel):
    message_class: str
    message: str


class ChatHistory:
    def __init__(self, redis: Redis, session_id: str):
        self.redis = redis
        self.session_id = session_id
        self.expiration_time = 60 * 60  # 1 hour

    def _key(self) -> str:
        return f"history:{self.session_id}"

    async def _get_history(self) -> list[dict[str, str]]:
        raw_history = self.redis.get(self._key())
        if raw_history is None:
            return []

        return json.loads(raw_history)

    async def _save_history(self, history: list[dict[str, str]]):
        self.redis.set(self._key(), json.dumps(history), ex=self.expiration_time)

    async def add_message(self, message_class: str, message: str):
        message_ = Message(message_class=message_class, message=message)
        history = await self._get_history()
        history.append(message_.dict())
        await self._save_history(history)

    async def get_messages(self) -> list[tuple[str, str]]:
        history = await self._get_history()
        return [(message["message_class"], message["message"]) for message in history]


def get_chat_history_whatsapp(redis: Redis, user: CurrentUserWA):
    return ChatHistory(redis, "wa:" + str(user.uuid))
