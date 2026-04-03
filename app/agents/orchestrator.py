# app/agents/orchestrator.py

from app.services.intent_service import detect_intent

from app.agents.calendar_agent import calendar_agent
from app.agents.task_agent import task_agent
from app.agents.memory_agent import memory_agent


def handle_request(query: str):
    try:
        print("🤖 Processing query...")

        intent = detect_intent(query)
        print("🧠 Detected intent:", intent)

        agents_used = []
        actions = []

        # 🔥 Intent-based routing (REAL LOGIC)

        if intent == "calendar":
            agents_used.append("CalendarAgent")
            actions.append(
                calendar_agent.tools[0]({
                    "title": "Meeting",
                    "time": "Tomorrow 10 AM"
                })
            )

        elif intent == "task":
            agents_used.append("TaskAgent")
            actions.append(
                task_agent.tools[0]({
                    "task": "Prepare slides"
                })
            )

        elif intent == "knowledge":
            agents_used.append("KnowledgeAgent")
            actions.append(f"🧠 Answering: {query}")

        # Always memory
        agents_used.append("MemoryAgent")
        actions.append(memory_agent.tools[0](query))

        decision = ", ".join(agents_used)

        print("✅ Agents used:", agents_used)

        return {
            "mode": "multi-agent",
            "decision": f"{decision} selected",
            "agents_used": agents_used,
            "actions": actions
        }

    except Exception as e:
        print("⚠️ System failed:", e)

        return {
            "mode": "error",
            "decision": "fallback",
            "agents_used": [],
            "actions": ["Something went wrong"]
        }