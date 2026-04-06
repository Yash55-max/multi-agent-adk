def detect_intent(query: str):
    q = query.lower()

    if "meeting" in q or "schedule" in q:
        return "calendar"
    elif "task" in q or "prepare" in q:
        return "task"
    else:
        return "knowledge"