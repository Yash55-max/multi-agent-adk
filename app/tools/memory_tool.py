from personal_assistant.memory_store import memory_db

def store_memory(query):
    memory_db.setdefault("history", []).append(query)
    return f"🧠 Stored memory: {query}"