import json
import logging
from datetime import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, WebSocket
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field, ValidationError

from taskmasterexp.auth.dependencies import CurrentUserWS

from ..dependencies import ChatAgent

logger = logging.getLogger(__name__)

router = APIRouter(tags="assistant")


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


@router.websocket("/chat/{token}")
async def chat_endpoint(
    websocket: WebSocket,
    agent: ChatAgent,
    user: CurrentUserWS,
):
    await websocket.accept()

    response_message = Message(
        text="Hello! How can I be of service?",
        sender="Helper",
    )
    await websocket.send_text(response_message.model_dump_json())

    while True:
        data = await websocket.receive_text()

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

        logger.info(f"Received message: {chat_input.message.text}")
        async for step in agent.astream(
            {
                "messages": [HumanMessage(chat_input.message.text)],
            },
            config={
                "configurable": {"thread_id": str(user.uuid)},
            },
            stream_mode="updates",
        ):
            logger.info(f"Step: {step}")
            final_result = step

        logger.info("Finish graph")
        try:
            response_message = Message(
                text=final_result["agent"]["messages"][-1].content,
                sender="Helper",
            )
            await websocket.send_text(response_message.model_dump_json())
        except Exception as e:
            logger.exception(e)
            response_message = Message(
                text="There was an error",
                sender="Helper",
            )
            await websocket.send_text(response_message.model_dump_json())
