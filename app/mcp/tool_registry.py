from app.tools.calendar_tool import create_event, list_meetings
from app.tools.task_tool import create_task, list_tasks


def create_task_tool(data):
    return create_task(data)


def get_tasks_tool(data):
    return list_tasks(data)


def create_meeting_tool(data):
    return create_event(data)


def get_meetings_tool(data):
    return list_meetings(data)


# 🔥 TOOL REGISTRY (MCP STYLE)
TOOLS = {
    "create_task": create_task,
    "get_tasks": list_tasks,

    "create_meeting": create_event,
    "get_meetings": list_meetings,
}