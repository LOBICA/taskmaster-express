import logging

from langchain_openai import ChatOpenAI

from taskmasterexp.settings import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE

logger = logging.getLogger(__name__)


def get_chat_model():
    logger.info(f"Setting up chat model {OPENAI_MODEL}")
    return ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
        temperature=OPENAI_TEMPERATURE,
    )
