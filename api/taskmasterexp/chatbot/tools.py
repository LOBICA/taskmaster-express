from datetime import datetime

from langchain_core.tools import tool


@tool
def get_current_time() -> str:
    """Return the current time in ISO format."""
    return datetime.now().isoformat()


tools = [get_current_time]
