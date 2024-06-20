from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder

from .client import chat_model

template = "You are a helpful assistant"
human_template = "{text}"


chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        MessagesPlaceholder(variable_name="history"),
        ("human", human_template),
    ]
)


chain = chat_prompt | chat_model
