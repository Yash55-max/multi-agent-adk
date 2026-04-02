from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.orchestrator import handle_request


class AskRequest(BaseModel):
    query: str


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Multi-Agent ADK System Running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
async def ask(payload: AskRequest):
    response = handle_request(payload.query)
    return {"response": response}
