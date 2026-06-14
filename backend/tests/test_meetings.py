import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock, patch
from io import BytesIO
from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_list_meetings_empty():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/meetings/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_process_meeting_mocked():
    mock_transcript = "Alice will finish the report by Friday. We decided to launch on Monday."
    mock_intelligence = {
        "summary": "Team discussed launch timeline.",
        "action_items": [{"task": "Finish report", "owner": "Alice", "due": "2026-06-20", "priority": "HIGH"}],
        "decisions": ["Launch on Monday"],
        "open_questions": []
    }
    with patch("app.routes.meetings.transcribe_audio", new_callable=AsyncMock, return_value=mock_transcript), \
         patch("app.routes.meetings.extract_meeting_intelligence", new_callable=AsyncMock, return_value=mock_intelligence), \
         patch("app.routes.meetings.send_summary_email", new_callable=AsyncMock):
        audio_bytes = b"fake audio data"
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/meetings/process",
                files={"audio": ("meeting.wav", BytesIO(audio_bytes), "audio/wav")}
            )
    assert response.status_code == 200
    data = response.json()
    assert "meeting_id" in data
    assert data["summary"] == "Team discussed launch timeline."
    assert len(data["action_items"]) == 1
    assert data["decisions"] == ["Launch on Monday"]


@pytest.mark.asyncio
async def test_get_meeting_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/meetings/mtg_doesnotexist")
    assert response.status_code == 404
