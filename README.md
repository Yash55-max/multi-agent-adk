# Multi-Agent ADK

A minimal multi-agent productivity API using FastAPI and Google ADK.

## Project Structure

```text
multi-agent-adk/
|-- app/
|   |-- main.py
|   |-- agents/
|   |   |-- orchestrator.py
|   |   |-- calendar_agent.py
|   |   |-- task_agent.py
|   |   `-- memory_agent.py
|   |-- tools/
|   |   |-- calendar_tool.py
|   |   |-- task_tool.py
|   |   `-- memory_tool.py
|   `-- services/
|       `-- llm_service.py
|-- requirements.txt
|-- Dockerfile
|-- .env
`-- README.md
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your API key to `.env`:

```env
GOOGLE_API_KEY=your_api_key_here
```

4. Run the app:

```bash
uvicorn app.main:app --reload
```

## API

### Health

- `GET /health`

### Ask

- `POST /ask`
- Body:

```json
{
  "query": "Schedule a meeting tomorrow at 10 AM and create a task to prepare slides"
}
```

Example with curl:

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"Schedule a meeting tomorrow at 10 AM and create a task to prepare slides\"}"
```

## Docker

```bash
docker build -t multi-agent-adk .
docker run -p 8080:8080 --env-file .env multi-agent-adk
```
