import asyncio
import logging
from typing import Annotated

from fastapi import APIRouter, Form, status

from taskmasterexp.settings import WHATSAPP_NUMBER

from .dependencies import ChatHistoryWA, TwilioClient, WhatsAppAgent
from .errors import MessageTooLongError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/messages", tags=["messages"])


async def _send_split_message(client: TwilioClient, text: str, destination: str):
    messages = []
    char_count = 0

    paragraphs = text.split("\n")

    if any(len(paragraph) > 1300 for paragraph in paragraphs):
        raise MessageTooLongError

    for paragraph in paragraphs:
        paragraph_len = len(paragraph)
        char_count += paragraph_len
        if char_count > 1300:
            _send_message(client, "\n".join(messages), destination=destination)
            messages = []
            char_count = paragraph_len
            # Add a delay between messages
            await asyncio.sleep(1)
        messages.append(paragraph)
    _send_message(client, "\n".join(messages), destination=destination)


def _send_message(client: TwilioClient, text: str, destination: str):
    client.messages.create(
        from_=f"whatsapp:{WHATSAPP_NUMBER}", body=text, to=destination
    )


async def _invoke_agent(agent: WhatsAppAgent, history: ChatHistoryWA, text: str):
    messages = await history.get_messages()
    response = await agent.ainvoke(
        {
            "history": messages,
            "text": text,
        }
    )
    await history.add_message("human", text)
    await history.add_message("ai", response["output"])
    return response


@router.post("/webhook", status_code=status.HTTP_204_NO_CONTENT)
async def receive_message(
    agent: WhatsAppAgent,
    history: ChatHistoryWA,
    twilio: TwilioClient,
    From: Annotated[str, Form()],
    Body: Annotated[str, Form()],
):
    logger.info(f"Received message: {Body}")
    try:
        response = await _invoke_agent(agent, history, Body)
        if len(response["output"]) > 1300:
            try:
                await _send_split_message(twilio, response["output"], destination=From)
            except MessageTooLongError:
                response = await _invoke_agent(
                    agent, history, "Please shorten your answer"
                )
                await _send_split_message(twilio, response["output"], destination=From)
        else:
            _send_message(twilio, response["output"], destination=From)
    except Exception as e:
        logger.exception(e)
        _send_message(twilio, "Sorry, an error occurred", destination=From)
