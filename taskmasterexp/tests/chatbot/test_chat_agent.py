from unittest.mock import patch

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from taskmasterexp.ai.assistants.chat_agent import get_chat_agent


async def test_get_chat_agent(chat_model_mock, test_admin_user):
    with patch("taskmasterexp.ai.assistants.chat_agent.ChatModel", chat_model_mock):
        agent = await get_chat_agent(test_admin_user, MemorySaver())
        assert agent is not None

        async for step in agent.astream(
            {
                "messages": [HumanMessage("Hello")],
            },
            config={
                "configurable": {"thread_id": str(test_admin_user.uuid)},
            },
            stream_mode="updates",
        ):
            final_result = step

        assert final_result["agent"]["messages"][-1].content == "response"
