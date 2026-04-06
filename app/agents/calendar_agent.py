from google.adk import Agent
from app.tools.calendar_tool import create_event

calendar_agent = Agent(
    name="CalendarAgent",
    description="Handles scheduling meetings",
    tools=[create_event],
)