from google.adk import Agent

from app.tools.task_tool import create_task

task_agent = Agent(
    name="TaskAgent",
    description="Manages tasks and todos",
    tools=[create_task],
)
from personal_assistant.memory_store import memory_db

def create_event(data):
    memory_db["meetings"].append(data)
    return f"✅ Meeting scheduled: {data}"