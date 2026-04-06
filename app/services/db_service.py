from google.cloud import firestore

db = firestore.Client()

# 📅 MEETINGS
def insert_meeting(title, time):
    db.collection("meetings").add({
        "title": title,
        "time": time
    })
    return f"📅 Meeting stored: {title} at {time}"


def get_meetings():
    docs = db.collection("meetings").stream()
    return [doc.to_dict() for doc in docs]


# ✅ TASKS
def insert_task(task):
    db.collection("tasks").add({
        "task": task
    })
    return f"✅ Task stored: {task}"


def get_tasks():
    docs = db.collection("tasks").stream()
    return [doc.to_dict() for doc in docs]