import logging
from typing import Annotated

from fastapi import APIRouter, Form, status
from twilio.rest import Client

from taskmasterexp.settings import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    WHATSAPP_NUMBER,
)

from .dependencies import ChatHistoryWA, WhatsAppAgent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/messages", tags=["messages"])

_client = None


def get_twilio_client():
    global _client
    if _client is None:
        _client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    return _client


def _send_message(text: str, destination: str):
    client = get_twilio_client()
    client.messages.create(
        from_=f"whatsapp:{WHATSAPP_NUMBER}", body=text, to=destination
    )


@router.post("/webhook", status_code=status.HTTP_204_NO_CONTENT)
async def receive_message(
    agent: WhatsAppAgent,
    history: ChatHistoryWA,
    From: Annotated[str, Form()],
    Body: Annotated[str, Form()],
):
    logger.info(f"Received message: {Body}")
    messages = await history.get_messages()
    response = await agent.ainvoke(
        {
            "history": messages,
            "text": Body,
        }
    )
    _send_message(response["output"], destination=From)
    await history.add_message("human", Body)
    await history.add_message("ai", response["output"])
