from google.adk import Agent

from app.tools.task_tool import create_task

task_agent = Agent(
    name="TaskAgent",
    description="Manages tasks and todos",
    tools=[create_task],
)
