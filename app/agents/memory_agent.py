from google.adk import Agent
from app.tools.memory_tool import store_memory

memory_agent = Agent(
    name="MemoryAgent",
    description="Stores user memory",
    tools=[store_memory],
)