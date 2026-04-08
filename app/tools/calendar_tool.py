from app.services.db_service import insert_meeting, get_meetings


def create_event(data):
    if not isinstance(data, dict):
        return "⚠️ Invalid meeting data"

    title = data.get("title")
    time = data.get("time")

    if not title:
        return "⚠️ Missing meeting title"

    return insert_meeting(title, time)


def list_meetings(time_filter=None):
    return get_meetings(time_filter)