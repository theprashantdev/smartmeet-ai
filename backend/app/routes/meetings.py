import json
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.db.session import get_db
from app.db.models import Meeting
from app.services.transcriber import transcribe_audio
from app.services.extractor import extract_meeting_intelligence
from app.services.emailer import send_summary_email
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/meetings", tags=["meetings"])

@router.post("/process")
async def process_meeting(
    audio: UploadFile = File(...),
    attendee_emails: str = "",
    db: AsyncSession = Depends(get_db)
):
    audio_bytes = await audio.read()
    transcript = await transcribe_audio(audio_bytes, audio.filename)
    intelligence = await extract_meeting_intelligence(transcript)

    meeting = Meeting(
        filename=audio.filename,
        transcript=transcript,
        summary=intelligence.get("summary", ""),
        action_items=intelligence.get("action_items", []),
        decisions=intelligence.get("decisions", []),
        open_questions=intelligence.get("open_questions", []),
    )
    db.add(meeting)
    await db.commit()
    await db.refresh(meeting)

    if attendee_emails:
        emails = [e.strip() for e in attendee_emails.split(",") if e.strip()]
        await send_summary_email(emails, intelligence, f"Meeting Summary — {audio.filename}")

    return {"meeting_id": meeting.id, **intelligence}

@router.get("/{meeting_id}")
async def get_meeting(meeting_id: str, db: AsyncSession = Depends(get_db)):
    m = await db.get(Meeting, meeting_id)
    if not m:
        raise HTTPException(404, "Meeting not found")
    return {"id": m.id, "summary": m.summary, "action_items": m.action_items,
            "decisions": m.decisions, "open_questions": m.open_questions, "created_at": str(m.created_at)}

@router.get("/")
async def list_meetings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Meeting).order_by(desc(Meeting.created_at)).limit(50))
    return [{"id": m.id, "filename": m.filename, "summary": m.summary, "created_at": str(m.created_at)}
            for m in result.scalars().all()]
