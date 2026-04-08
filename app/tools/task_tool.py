from app.services.db_service import insert_task, get_tasks


def create_task(data):
    # 🔥 HANDLE BAD INPUT
    if not isinstance(data, dict):
        return "⚠️ Invalid task data"

    task = data.get("task")
    time = data.get("time")

    if not task:
        return "⚠️ Task missing"

    return insert_task(task, time)


def list_tasks(time_filter=None):
    return get_tasks(time_filter)