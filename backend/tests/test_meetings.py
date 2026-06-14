import pytest
from unittest.mock import AsyncMock, patch
from io import BytesIO


@pytest.mark.asyncio
async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_list_meetings_empty(client):
    r = await client.get("/api/meetings/")
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_get_meeting_not_found(client):
    r = await client.get("/api/meetings/mtg_doesnotexist")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_process_meeting_mocked(client):
    mock_transcript = "Alice will finish the report by Friday."
    mock_intelligence = {
        "summary": "Discussed launch timeline.",
        "action_items": [{"task": "Finish report", "owner": "Alice", "due": "2026-06-20", "priority": "HIGH"}],
        "decisions": ["Launch on Monday"],
        "open_questions": []
    }
    with patch("app.routes.meetings.transcribe_audio", new_callable=AsyncMock, return_value=mock_transcript), \
         patch("app.routes.meetings.extract_meeting_intelligence", new_callable=AsyncMock, return_value=mock_intelligence), \
         patch("app.routes.meetings.send_summary_email", new_callable=AsyncMock):
        r = await client.post(
            "/api/meetings/process",
            files={"audio": ("meeting.wav", BytesIO(b"fake audio data"), "audio/wav")}
        )
    assert r.status_code == 200
    d = r.json()
    assert "meeting_id" in d
    assert d["summary"] == "Discussed launch timeline."
    assert d["decisions"] == ["Launch on Monday"]
