from google.adk import Agent

from app.agents.calendar_agent import calendar_agent
from app.agents.memory_agent import memory_agent
from app.agents.task_agent import task_agent

orchestrator = Agent(
    name="Orchestrator",
    description="""
    You are a smart productivity assistant.

    Your job:
    - Understand user requests
    - Delegate tasks to appropriate agents

    Available agents:
    - CalendarAgent -> scheduling
    - TaskAgent -> task management
    - MemoryAgent -> storing information
    """,
    sub_agents=[calendar_agent, task_agent, memory_agent],
)


def handle_request(query: str):
    return orchestrator.run(query)
