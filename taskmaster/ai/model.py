import logging

from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState

from taskmaster.settings import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE

logger = logging.getLogger(__name__)


def get_chat_model():
    return ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
        temperature=OPENAI_TEMPERATURE,
    )


class ChatModel:
    def __init__(self, system_messages: list, tools: list = []):
        self.system_messages = system_messages
        self.tools = tools

        if tools:
            self.model = get_chat_model().bind_tools(tools)
        else:
            self.model = get_chat_model()

    async def call(self, state: MessagesState, config: RunnableConfig):
        messages = state["messages"]
        response = await self.model.ainvoke(
            self.system_messages + messages,
            config,
        )
        return {"messages": [response]}
