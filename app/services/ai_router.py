from google import genai
import os
import json

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 🔥 FALLBACK (RULE-BASED AI)
def fallback_parser(query: str):
    q = query.lower()

    if "task" in q:
        if "show" in q or "list" in q:
            return {
                "action": "get_tasks",
                "time": "today" if "today" in q else None
            }
        return {
            "action": "create_task",
            "task": q,
            "time": "today" if "today" in q else "unknown"
        }

    if "meeting" in q or "schedule" in q:
        if "show" in q:
            return {
                "action": "get_meetings",
                "time": "today" if "today" in q else None
            }
        return {
            "action": "create_meeting",
            "title": q,
            "time": "today" if "today" in q else "unknown"
        }

    if "help" in q or "what" in q:
        return {"action": "help"}

    return {"action": "chat"}


# 🔥 MAIN AI FUNCTION
def parse_user_input(query: str):
    prompt = f"""
Convert user input into structured JSON.

Actions:
- create_task
- get_tasks
- create_meeting
- get_meetings
- help
- chat

Rules:
- Extract clean task/meeting title (remove words like add, schedule, etc.)
- Extract time if mentioned (today, tomorrow, 9am etc.)
- Keep task short and meaningful

Examples:

Input: add task gym today
Output: {{"action":"create_task","task":"gym","time":"today"}}

Input: add a reading task for tomorrow 9 am
Output: {{"action":"create_task","task":"reading","time":"tomorrow 9 am"}}

Input: schedule meeting with team tomorrow
Output: {{"action":"create_meeting","title":"meeting with team","time":"tomorrow"}}

Input: show tasks today
Output: {{"action":"get_tasks","time":"today"}}

Return ONLY JSON.

Input: {query}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        text = response.text.strip()

        if "```" in text:
            text = text.split("```")[1]

        return json.loads(text)

    except Exception as e:
        print("⚠️ AI failed, using fallback:", e)

        # 🔥 THIS IS THE IMPORTANT LINE
        return fallback_parser(query)