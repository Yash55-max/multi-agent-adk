from google.adk import Agent

from app.tools.calendar_tool import create_event

calendar_agent = Agent(
    name="CalendarAgent",
    description="Handles scheduling and calendar events",
    tools=[create_event],
)
