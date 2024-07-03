from typing import Annotated

from fastapi import Depends

from . import assistant


ChatAgent = Annotated[assistant.AgentExecutor, Depends(assistant.get_chat_agent)]
WhatsAppAgent = Annotated[
    assistant.AgentExecutor, Depends(assistant.get_whatsapp_chat_agent)
]

