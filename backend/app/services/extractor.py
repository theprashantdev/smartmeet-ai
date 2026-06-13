import httpx
import json
from app.core.config import settings

EXTRACTION_PROMPT = """Analyze this meeting transcript and extract:
1. A concise summary (3-5 sentences)
2. Action items with owner names and due dates mentioned (or infer 1 week if not stated)
3. Key decisions made
4. Open questions not resolved

Transcript:
{transcript}

Respond ONLY in this JSON format:
{
  "summary": "...",
  "action_items": [{"task": "...", "owner": "...", "due": "YYYY-MM-DD", "priority": "HIGH|MEDIUM|LOW"}],
  "decisions": ["..."],
  "open_questions": ["..."]
}"""

async def extract_meeting_intelligence(transcript: str) -> dict:
    prompt = EXTRACTION_PROMPT.format(transcript=transcript[:8000])
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.openrouter_api_key}", "Content-Type": "application/json"},
            json={
                "model": settings.openrouter_model,
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"},
                "temperature": 0.1,
            }
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)
