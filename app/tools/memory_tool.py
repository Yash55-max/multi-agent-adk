memory_store = []


def store_memory(data: str) -> str:
    memory_store.append(data)
    return f"Stored memory: {data}"
