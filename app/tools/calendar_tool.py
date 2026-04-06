from app.services.db_service import insert_meeting

def create_event(data):
    return insert_meeting(data["title"], data["time"])