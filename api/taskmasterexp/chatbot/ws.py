import json
import logging
from datetime import date, datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, WebSocket
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)

router = APIRouter(tags="chatbot")


class Message(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    text: str
    timestamp: datetime = Field(default_factory=date.today)
    sender: str


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
            message = Message(**json_data)
        except (json.JSONDecodeError, ValidationError) as e:
            logger.exception(e)
            logger.error(f"Invalid message: {data}")
            continue

        message = Message(
            text=f"Message text was: {message.text}",
            sender="Helper",
        )
        await websocket.send_text(message.json())
