import logging
from typing import Annotated

from fastapi import APIRouter, Form, status
from langchain_core.messages import HumanMessage

from taskmasterexp.auth.dependencies import CurrentUserWA
from taskmasterexp.twilio.dependencies import TwilioClient
from taskmasterexp.twilio.errors import MessageTooLongError
from taskmasterexp.twilio.utils import send_message, send_split_message

from ..dependencies import WhatsAppAgent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/messages", tags=["messages"])


async def _invoke_agent(agent: WhatsAppAgent, user_uuid: str, text: str):
    async for step in agent.astream(
        {
            "messages": [HumanMessage(text)],
        },
        config={
            "configurable": {"thread_id": "wa-" + str(user_uuid)},
        },
        stream_mode="updates",
    ):
        logger.info(f"Step: {step}")
        final_result = step

    return final_result["agent"]["messages"][-1].content


@router.post("/webhook", status_code=status.HTTP_204_NO_CONTENT)
async def receive_message(
    agent: WhatsAppAgent,
    user: CurrentUserWA,
    twilio: TwilioClient,
    From: Annotated[str, Form()],
    Body: Annotated[str, Form()],
):
    logger.info(f"Received message: {Body}")
    try:
        response = await _invoke_agent(agent, str(user.uuid), Body)
        if len(response) > 1300:
            try:
                await send_split_message(twilio, response, destination=From)
            except MessageTooLongError:
                response = await _invoke_agent(
                    agent, str(user.uuid), "Please shorten your answer"
                )
                await send_split_message(twilio, response, destination=From)
        else:
            send_message(twilio, response, destination=From)
    except Exception as e:
        logger.exception(e)
        send_message(twilio, "Sorry, an error occurred", destination=From)
