from fastapi import FastAPI
from pydantic import BaseModel
from app.agents.orchestrator import handle_request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


class AskRequest(BaseModel):
    query: str


@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
async def ask(payload: AskRequest):
    try:
        print("➡️ Incoming Query:", payload.query)

        response = handle_request(payload.query)

        print("✅ Response:", response)

        return {
            "success": True,
            "query": payload.query,
            "response": response
        }

    except Exception as e:
        print("❌ Error:", str(e))

        return {
            "success": False,
            "error": str(e)
        }