# personal_assistant/agent.py

from google.adk import Agent
from personal_assistant.memory_store import memory_db


# 🔧 TOOLS

def create_event(data):
    event = {
        "title": str(data),
        "time": "tomorrow"
    }

    memory_db["meetings"].append(event)

    # 🔥 auto-create task
    memory_db["tasks"].append(f"Prepare for {event['title']}")

    return f"✅ Meeting scheduled: {event}"


def create_task(data):
    task = str(data)
    memory_db["tasks"].append(task)
    return f"✅ Task created: {task}"


def get_tasks(_):
    if not memory_db["tasks"]:
        return "📋 No tasks found"

    return f"📋 Tasks: {memory_db['tasks']}"


# 🤖 SUB-AGENTS

calendar_agent = Agent(
    name="CalendarAgent",
    description="Schedules meetings",
    tools=[create_event]
)

task_agent = Agent(
    name="TaskAgent",
    description="Manages tasks",
    tools=[get_tasks]
)

memory_agent = Agent(
    name="MemoryAgent",
    description="Stores and retrieves information",
    tools=[]
)


# 🧠 ROOT AGENT (ORCHESTRATOR)

root_agent = Agent(
    name="Orchestrator",
    description="""
    You are a productivity assistant.

    IMPORTANT:
    - Use tools directly when possible
    - Do NOT overthink or ask unnecessary questions
    - Execute tasks immediately

    Agents:
    - CalendarAgent → scheduling
    - TaskAgent → tasks
    """,
    sub_agents=[
        calendar_agent,
        task_agent,
        memory_agent
    ]
)