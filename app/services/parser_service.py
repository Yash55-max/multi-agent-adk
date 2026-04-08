import re

def fallback_parser(query: str):
    q = query.lower()

    # ⏰ TIME
    time = None
    if "today" in q:
        time = "today"
    elif "tomorrow" in q:
        time = "tomorrow"

    # ⏰ TIME WITH HOURS
    time_match = re.search(r"\b\d{1,2}\s?(am|pm)\b", q)
    if time_match:
        time = f"{time or ''} {time_match.group()}".strip()

    # ✅ TASK
    if "task" in q:
        if "show" in q:
            return {"action": "get_tasks", "time": time}

        # remove junk words
        clean = re.sub(r"(add|create|task|a|the|for)", "", q).strip()

        return {
            "action": "create_task",
            "task": clean,
            "time": time or "unknown"
        }

    # 📅 MEETING
    if "meeting" in q or "schedule" in q:
        if "show" in q:
            return {"action": "get_meetings", "time": time}

        clean = re.sub(r"(schedule|meeting|a|the|for)", "", q).strip()

        return {
            "action": "create_meeting",
            "title": clean or "meeting",
            "time": time or "unknown"
        }

    if "help" in q or "what" in q:
        return {"action": "help"}

    return {"action": "chat"}