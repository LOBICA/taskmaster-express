import logging
from typing import Literal

from langchain.agents import AgentExecutor
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from taskmasterexp.helpers import get_current_time, get_weekday
from taskmasterexp.schemas.tasks import Task
from taskmasterexp.schemas.users import User

from ..checkpoint.redis import AsyncRedisSaver
from ..client import get_chat_model
from ..tools import tools

logger = logging.getLogger(__name__)


async def get_chat_agent(user: User, checkpointer: AsyncRedisSaver) -> AgentExecutor:
    task_template = "[title]\n[description]\nStatus: [status]\n"

    if not user.email:
        email_message = (
            "The user does not have an email address associated,"
            " ask for an email address when you greet them."
            " Be polite and only ask once."
        )
    else:
        email_message = (
            "The user already has an email address, "
            "we won't be able to associate a new one"
        )

    system_messages = [
        SystemMessage("You are an assistant helping the user to organize their tasks"),
        SystemMessage("The url for the aplication is https://helpitdone.com"),
        SystemMessage(f"The user's uuid is {user.uuid}"),
        HumanMessage(f"My name is {user.name}"),
        SystemMessage(f"The task format is: <{Task.ai_format_template()}>"),
        SystemMessage("You will list the tasks as: \n1.[title]\n2.[title]\n..."),
        SystemMessage("If the task list is empty you will say that there are no tasks"),
        SystemMessage(
            "When giving more details about a tasks "
            f"you will present them as {task_template}."
        ),
        SystemMessage(f"Today is {get_weekday()}, {get_current_time()}"),
        SystemMessage(email_message),
    ]

    def should_continue(state: MessagesState) -> Literal["tools", END]:
        messages = state["messages"]
        last_message = messages[-1]
        # If the LLM makes a tool call, then we route to the "tools" node
        if last_message.tool_calls:
            logger.info("Calling tools")
            return "tools"
        # Otherwise, we stop (reply to the user)
        return END

    async def call_model(state: MessagesState, config: RunnableConfig):
        model = get_chat_model().bind_tools(tools)
        messages = state["messages"]
        response = await model.ainvoke(
            system_messages + messages,
            config,
        )
        return {"messages": [response]}

    workflow = StateGraph(MessagesState)

    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue)
    workflow.add_edge("tools", "agent")

    app = workflow.compile(checkpointer=checkpointer)

    return app
