def detect_intent(query: str):
    query = query.lower()

    if any(word in query for word in ["meeting", "schedule", "appointment"]):
        return "calendar"

    elif any(word in query for word in ["task", "todo", "prepare", "complete"]):
        return "task"

    elif any(word in query for word in ["remember", "note", "store"]):
        return "memory"

    elif any(word in query for word in ["what", "explain", "tell"]):
        return "knowledge"

    else:
        return "memory"