from google.adk import Agent
from app.tools.calendar_tool import create_event, list_meetings

calendar_agent = Agent(
    name="CalendarAgent",
    description="Handles scheduling",
    tools=[create_event, list_meetings],
)