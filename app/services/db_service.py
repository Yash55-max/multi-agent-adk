from google.cloud import firestore

db = firestore.Client()

# =========================
# 📅 MEETINGS
# =========================
def insert_meeting(title, date="unknown", time="unknown"):
    date = date or "unknown"
    time = time or "unknown"

    db.collection("meetings").add({
        "title": title,
        "date": date,
        "time": time
    })

    return f"📅 Meeting stored: {title} ({date} {time})"


def get_meetings(date_filter=None):
    docs = db.collection("meetings").stream()
    meetings = [doc.to_dict() for doc in docs]

    if date_filter:
        meetings = [m for m in meetings if m.get("date") == date_filter]

    if not meetings:
        return "📭 No meetings found"

    return "\n".join([
        f"• {m.get('title', 'meeting')} ({m.get('date', 'unknown')} {m.get('time', 'unknown')})"
        for m in meetings
    ])


# =========================
# ✅ TASKS
# =========================
def insert_task(task, date="unknown", time="unknown"):
    date = date or "unknown"
    time = time or "unknown"

    db.collection("tasks").add({
        "task": task,
        "date": date,
        "time": time
    })

    return f"✅ Task stored: {task} ({date} {time})"


def get_tasks(date_filter=None):
    docs = db.collection("tasks").stream()
    tasks = [doc.to_dict() for doc in docs]

    if date_filter:
        tasks = [t for t in tasks if t.get("date") == date_filter]

    if not tasks:
        return "📭 No tasks found"

    return "\n".join([
        f"• {t.get('task', 'task')} ({t.get('date', 'unknown')} {t.get('time', 'unknown')})"
        for t in tasks
    ])