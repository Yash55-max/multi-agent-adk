from google.adk import Agent
from app.tools.task_tool import create_task, list_tasks

task_agent = Agent(
    name="TaskAgent",
    description="Manages tasks",
    tools=[create_task, list_tasks],
)