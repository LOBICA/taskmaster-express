import json
import logging
from datetime import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, WebSocket
from pydantic import BaseModel, Field, ValidationError

from taskmasterexp.auth.dependencies import CurrentUser

from .assistant import chain

logger = logging.getLogger(__name__)

router = APIRouter(tags="chatbot")


class Message(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    text: str
    timestamp: datetime = Field(default_factory=datetime.now)
    sender: str

    @property
    def message_class(self):
        return "ai" if self.sender == "Helper" else "human"


class ChatInput(BaseModel):
    message: Message
    history: list[Message]


@router.websocket("/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        logger.info(f"Received data: {data}")

        if data == "close":
            await websocket.close()
            break

        if data == '{"isTrusted":true}':
            continue

        try:
            json_data = json.loads(data)
            chat_input = ChatInput(**json_data)
        except (json.JSONDecodeError, ValidationError) as e:
            logger.exception(e)
            logger.error(f"Invalid message: {data}")
            continue

        response = await chain.ainvoke(
            {
                "history": [
                    (message.message_class, message.text)
                    for message in chat_input.history
                ],
                "text": chat_input.message.text,
            }
        )

        response_message = Message(
            text=response.content,
            sender="Helper",
        )
        await websocket.send_text(response_message.json())
