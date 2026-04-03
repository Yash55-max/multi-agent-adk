from google.adk import Agent

from app.tools.calendar_tool import create_event

calendar_agent = Agent(
    name="CalendarAgent",
    description="Handles scheduling and calendar events",
    tools=[create_event],
)
from personal_assistant.memory_store import memory_db

def create_event(data):
    memory_db["meetings"].append(data)
    return f"✅ Meeting scheduled: {data}"