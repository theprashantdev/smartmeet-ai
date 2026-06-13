# 🎤 SmartMeet AI

> Record a meeting. Get a structured summary, action items with owners, and decisions logged — all automatically.

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?style=flat-square&logo=fastapi)]()
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-orange?style=flat-square&logo=openai)]()
[![React](https://img.shields.io/badge/React-18-blue?style=flat-square&logo=react)]()
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

## The Problem

After every meeting, someone has to manually write notes, figure out who owns what, and send a summary email. That takes 20-40 minutes and still misses things.

SmartMeet AI does all of it in under 60 seconds.

## What It Does

1. **Upload** a meeting audio file (mp3/wav/m4a) or record live
2. **Transcribes** using OpenAI Whisper (local or API)
3. **Extracts** using LLM:
   - Action items with assigned owners and due dates
   - Key decisions made
   - Open questions / unresolved items
   - Meeting summary (3-5 sentences)
4. **Emails** a formatted summary to all attendees
5. **Stores** everything searchable for future reference

## Architecture

```
┌───────────┐  audio   ┌─────────────┐  text   ┌───────────────┐
│  React  │──────▶│   Whisper    │──────▶│  LLM Extractor  │
│  UI     │        │   (STT)      │        │  (OpenRouter)   │
└───────────┘        └─────────────┘        └────────┬──────┘
                                                      │
                   ┌─────────┐  results        │
                   │ PostgreSQL│◀──────────────┘
                   └─────────┘
                        │
                   ┌─────────┐
                   │  Email    │
                   │  Service  │
                   └─────────┘
```

## Quick Start

```bash
git clone https://github.com/theprashantdev/smartmeet-ai
cd smartmeet-ai

# Backend
cd backend && pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend && npm install && npm run dev
```

Open `http://localhost:5173`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/meetings/process` | Upload audio, get full analysis |
| GET | `/api/meetings/{id}` | Get meeting by ID |
| GET | `/api/meetings/` | List all processed meetings |
| GET | `/api/meetings/{id}/actions` | Get action items only |
| POST | `/api/meetings/{id}/email` | Resend email summary |

## Sample Output

```json
{
  "meeting_id": "mtg_abc123",
  "duration_seconds": 1847,
  "summary": "Team aligned on Q3 launch date. Backend team to complete API by July 15. Design approved.",
  "action_items": [
    { "task": "Complete authentication API", "owner": "Rahul", "due": "2026-07-15", "priority": "HIGH" },
    { "task": "Update landing page copy", "owner": "Priya", "due": "2026-07-10", "priority": "MEDIUM" }
  ],
  "decisions": [
    "Q3 launch date confirmed as August 1, 2026",
    "Postgres chosen over MongoDB for main database"
  ],
  "open_questions": [
    "Pricing model for enterprise tier not yet finalized"
  ]
}
```

## Project Structure

```
smartmeet-ai/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/meetings.py
│   │   ├── services/
│   │   │   ├── transcriber.py    # Whisper integration
│   │   │   ├── extractor.py      # LLM extraction
│   │   │   └── emailer.py        # Summary email
│   │   ├── db/
│   │   │   └── models.py
│   │   └── core/config.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── UploadZone.tsx
│   │   │   ├── MeetingSummary.tsx
│   │   │   └── ActionTable.tsx
│   │   └── api/client.ts
│   └── package.json
└── README.md
```

## License

MIT © [Prashant Raj](https://github.com/theprashantdev)
