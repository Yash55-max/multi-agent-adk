# app/services/llm_service.py

import vertexai
from vertexai.generative_models import GenerativeModel

# ✅ Initialize ONCE (global level)
vertexai.init(
    project="yash-genai-final",
    location="us-central1"
)

# ✅ Load model once
model = GenerativeModel("gemini-1.5-flash")

def generate_response(prompt: str):
    response = model.generate_content(prompt)
    return response.text