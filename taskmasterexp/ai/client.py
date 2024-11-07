import logging

from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState

from taskmasterexp.settings import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE

logger = logging.getLogger(__name__)


def get_chat_model():
    return ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
        temperature=OPENAI_TEMPERATURE,
    )


def get_model_call(system_messages: list, tools: list = []):
    async def model_call(state: MessagesState, config: RunnableConfig):
        model = get_chat_model()
        if tools:
            model = model.bind_tools(tools)

        messages = state["messages"]
        response = await model.ainvoke(
            system_messages + messages,
            config,
        )
        return {"messages": [response]}

    return model_call
