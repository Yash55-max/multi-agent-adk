from app.mcp.tool_registry import TOOLS
from app.agents.memory_agent import memory_agent
import re

# 🔥 STATE
pending_task = None
pending_meeting = None


# =========================
# 🧠 EXTRACT TIME + DATE
# =========================
def extract_time_and_date(text):
    text = text.lower().strip()

    # TIME → handles "9am", "9 am"
    time_match = re.search(r'(\d{1,2})\s*(am|pm)', text)
    time = None
    if time_match:
        time = f"{time_match.group(1)}{time_match.group(2)}"

    # DATE
    date = None
    if "today" in text:
        date = "today"
    elif "tomorrow" in text:
        date = "tomorrow"

    return time, date


def handle_request(query: str):
    try:
        print("🤖 Processing (clean AI)...")

        global pending_task, pending_meeting

        q = query.lower()

        agents_used = []
        actions = []
        trace = []

        commands = [
            cmd.strip() for cmd in q.replace(" and ", ",").split(",")
        ]

        for cmd in commands:

            step = {
                "command": cmd,
                "agent": None,
                "reason": None,
                "action": None
            }

            # =========================
            # 🔁 FOLLOW-UP TASK
            # =========================
            if pending_task and any(x in cmd for x in ["am", "pm"]):
                agents_used.append("TaskAgent")

                step["agent"] = "TaskAgent"
                step["reason"] = "Follow-up time for task"

                time, new_date = extract_time_and_date(cmd)

                result = TOOLS["create_task"]({
                    "task": pending_task["task"],
                    "date": new_date if new_date else pending_task.get("date", "unknown"),
                    "time": time if time else "unknown"
                })

                pending_task = None

                step["action"] = result
                actions.append(result)
                trace.append(step)
                continue

            # =========================
            # 🔁 FOLLOW-UP MEETING
            # =========================
            if pending_meeting and any(x in cmd for x in ["am", "pm"]):
                agents_used.append("CalendarAgent")

                step["agent"] = "CalendarAgent"
                step["reason"] = "Follow-up time for meeting"

                time, new_date = extract_time_and_date(cmd)

                result = TOOLS["create_meeting"]({
                    "title": pending_meeting["title"],
                    "date": new_date if new_date else pending_meeting.get("date", "unknown"),
                    "time": time if time else "unknown"
                })

                pending_meeting = None

                step["action"] = result
                actions.append(result)
                trace.append(step)
                continue

            # =========================
            # 📅 MEETING
            # =========================
            if "meeting" in cmd or "schedule" in cmd:

                agents_used.append("CalendarAgent")
                step["agent"] = "CalendarAgent"

                # 🔍 RETRIEVE
                if any(w in cmd for w in ["show", "display", "list", "get", "what", "see"]):
                    step["reason"] = "Meeting retrieval"
                    result = TOOLS["get_meetings"](None)

                # ➕ CREATE
                else:
                    step["reason"] = "Meeting creation"

                    # 🔥 EXTRACT FIRST
                    time, extracted_date = extract_time_and_date(cmd)

                    # 🔥 CLEAN TEXT
                    clean_title = re.sub(r'\d{1,2}\s*(am|pm)', '', cmd)
                    clean_title = re.sub(r'\b(today|tomorrow)\b', '', clean_title)

                    for word in ["schedule", "meeting", "with"]:
                        clean_title = clean_title.replace(word, "")

                    clean_title = clean_title.strip()

                    if not time:
                        pending_meeting = {
                            "title": clean_title or "meeting",
                            "date": extracted_date or "unknown"
                        }
                        result = "⏰ What time is the meeting?"
                    else:
                        result = TOOLS["create_meeting"]({
                            "title": clean_title or "meeting",
                            "date": extracted_date or "unknown",
                            "time": time
                        })

                step["action"] = result
                actions.append(result)

            # =========================
            # ✅ TASK
            # =========================
            elif "task" in cmd:

                agents_used.append("TaskAgent")
                step["agent"] = "TaskAgent"

                # 🔍 RETRIEVE
                if any(w in cmd for w in ["show", "display", "list", "get", "what", "see"]):
                    step["reason"] = "Task retrieval"
                    result = TOOLS["get_tasks"](None)

                # ➕ CREATE
                else:
                    step["reason"] = "Task creation"

                    # 🔥 EXTRACT FIRST
                    time, extracted_date = extract_time_and_date(cmd)

                    # 🔥 CLEAN TEXT
                    clean_task = re.sub(r'\d{1,2}\s*(am|pm)', '', cmd)
                    clean_task = re.sub(r'\b(today|tomorrow)\b', '', clean_task)

                    for word in ["add", "task", "for"]:
                        clean_task = clean_task.replace(word, "")

                    clean_task = clean_task.strip()

                    if not time:
                        pending_task = {
                            "task": clean_task or "task",
                            "date": extracted_date or "unknown"
                        }
                        result = "⏰ What time should I schedule this task?"
                    else:
                        result = TOOLS["create_task"]({
                            "task": clean_task or "task",
                            "date": extracted_date or "unknown",
                            "time": time
                        })

                step["action"] = result
                actions.append(result)

            # =========================
            # 👋 GREETING
            # =========================
            elif any(w in cmd for w in ["hi", "hello", "hey"]):
                agents_used.append("Assistant")
                step["agent"] = "Assistant"
                step["reason"] = "Greeting"

                result = "👋 Hey! I can manage tasks and meetings. Type 'help' to see options."

                step["action"] = result
                actions.append(result)

            # =========================
            # 🧠 HELP
            # =========================
            elif any(w in cmd for w in ["help", "capabilities"]):
                agents_used.append("Assistant")
                step["agent"] = "Assistant"
                step["reason"] = "Help"

                result = (
                    "🤖 I can:\n"
                    "• Add tasks → add task gym today 7am\n"
                    "• Show tasks → show tasks\n"
                    "• Schedule meetings → schedule meeting tomorrow 9am\n"
                    "• Show meetings → show meetings\n"
                )

                step["action"] = result
                actions.append(result)

            # =========================
            # ❌ UNKNOWN
            # =========================
            else:
                agents_used.append("System")
                step["agent"] = "System"
                step["reason"] = "Unknown"

                result = "⚠️ I didn’t understand. Try 'help'."

                step["action"] = result
                actions.append(result)

            trace.append(step)

        # =========================
        # 🧠 MEMORY
        # =========================
        agents_used.append("MemoryAgent")
        actions.append(memory_agent.tools[0](query))

        agents_used = list(set(agents_used))

        return {
            "mode": "clean-ai",
            "decision": ", ".join(agents_used),
            "agents_used": agents_used,
            "actions": actions,
            "trace": trace
        }

    except Exception as e:
        print("⚠️ Error:", e)

        return {
            "mode": "error",
            "decision": "fallback",
            "actions": ["Something went wrong"]
        }