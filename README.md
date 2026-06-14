# SmartMeet AI

Live Demo:
https://smartmeet-ai-yxjr.onrender.com

API Docs:
https://smartmeet-ai-yxjr.onrender.com/docs
> Upload a meeting audio file. Get back a transcript, action items with owners, decisions made, and an optional email summary — in under 60 seconds.

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?style=flat-square&logo=fastapi)]()
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-orange?style=flat-square)]()
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![CI](https://github.com/theprashantdev/smartmeet-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/theprashantdev/smartmeet-ai/actions/workflows/ci.yml)

## What It Does

1. You upload an audio file (`.wav`, `.mp3`, `.m4a`, `.ogg`)
2. Whisper transcribes the audio to text
3. OpenRouter extracts structured intelligence from the transcript:
   - Concise meeting summary
   - Action items with owner names and due dates
   - Key decisions made
   - Open questions not resolved
4. The result is stored in the database and optionally emailed to attendees

## Prerequisites

- Python 3.11+
- **ffmpeg** installed on the system (required by Whisper)
  - Ubuntu/Debian: `sudo apt-get install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows: download from https://ffmpeg.org/download.html
- PostgreSQL (or SQLite for local dev)

## Quick Start

```bash
git clone https://github.com/theprashantdev/smartmeet-ai
cd smartmeet-ai/backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env — set OPENROUTER_API_KEY and DATABASE_URL
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open **http://localhost:8000/docs** for interactive API docs.

For SQLite (no Postgres needed):
```env
DATABASE_URL=sqlite+aiosqlite:///./smartmeet.db
```

## Environment Variables

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=openai/gpt-4o-mini
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/smartmeet
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
WHISPER_MODEL=base
```

Email (SMTP) is optional. If `SMTP_USER` is empty, email sending is skipped silently.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/meetings/process` | Upload audio, get full meeting intelligence |
| `GET` | `/api/meetings/` | List all processed meetings |
| `GET` | `/api/meetings/{id}` | Get a specific meeting record |
| `GET` | `/health` | Health check |

## Example Request

```bash
curl -X POST http://localhost:8000/api/meetings/process \
  -F "audio=@recording.wav" \
  -F "attendee_emails=alice@company.com,bob@company.com"
```

```json
{
  "meeting_id": "mtg_3f9a1c2b7d4e",
  "summary": "Team aligned on Q3 launch timeline.",
  "action_items": [
    {"task": "Finalize spec doc", "owner": "Alice", "due": "2026-06-20", "priority": "HIGH"}
  ],
  "decisions": ["Launch on July 1st"],
  "open_questions": ["Who handles customer comms?"]
}
```

## Running Tests

Tests use SQLite in-memory and mock all external services — no database or API key needed.

```bash
cd backend
pytest --tb=short -v
```

## Docker

```bash
docker build -t smartmeet-ai .
docker run -p 8000:8000 --env-file backend/.env smartmeet-ai
```

## Architecture

```
POST /api/meetings/process
       │
       ▼
  Audio Upload (multipart)
       │
       ▼
  Whisper Transcription
  (run_in_executor — non-blocking)
       │
       ▼
  OpenRouter Extraction
  (summary + action items + decisions)
       │
       ▼
  Database Write
  (Meeting record)
       │
       ▼
  Email Summary (optional)
       │
       ▼
  Return JSON Response
```

## Project Structure

```
smartmeet-ai/
├── backend/
│   ├── app/
│   │   ├── core/config.py       # Pydantic settings
│   │   ├── db/models.py         # SQLAlchemy Meeting model
│   │   ├── db/session.py        # Async engine
│   │   ├── routes/meetings.py   # API routes
│   │   ├── services/
│   │   │   ├── transcriber.py   # Whisper (async-safe)
│   │   │   ├── extractor.py     # OpenRouter extraction
│   │   │   └── emailer.py       # SMTP summary email
│   │   └── main.py
│   ├── tests/
│   │   └── test_meetings.py
│   ├── conftest.py
│   ├── pytest.ini
│   ├── requirements.txt
│   └── .env.example
├── frontend/                    # React UI
├── Dockerfile
└── README.md
```

## License

MIT © [Prashant Raj](https://github.com/theprashantdev)
