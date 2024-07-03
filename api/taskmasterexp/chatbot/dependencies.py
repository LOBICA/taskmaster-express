from typing import Annotated

from fastapi import Depends

from . import assistant, history

ChatAgent = Annotated[assistant.AgentExecutor, Depends(assistant.get_chat_agent)]
WhatsAppAgent = Annotated[
    assistant.AgentExecutor, Depends(assistant.get_whatsapp_chat_agent)
]

ChatHistoryWA = Annotated[
    history.ChatHistory, Depends(history.get_chat_history_whatsapp)
]
