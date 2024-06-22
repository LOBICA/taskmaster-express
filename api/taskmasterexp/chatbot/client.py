from langchain_openai import ChatOpenAI

from taskmasterexp.settings import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE

chat_model = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model=OPENAI_MODEL,
    temperature=OPENAI_TEMPERATURE,
)
