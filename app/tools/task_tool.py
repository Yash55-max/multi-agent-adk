from app.services.db_service import insert_task

def create_task(data):
    return insert_task(data["task"])