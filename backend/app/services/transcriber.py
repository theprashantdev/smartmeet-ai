import asyncio
import tempfile
import os
from app.core.config import settings

_model = None

def _load_model():
    import whisper
    global _model
    if _model is None:
        _model = whisper.load_model(settings.whisper_model)
    return _model

def _transcribe_sync(audio_bytes: bytes, suffix: str) -> str:
    import whisper
    model = _load_model()
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        f.write(audio_bytes)
        tmp_path = f.name
    try:
        result = model.transcribe(tmp_path)
        return result["text"].strip()
    finally:
        os.unlink(tmp_path)

async def transcribe_audio(audio_bytes: bytes, filename: str) -> str:
    """Transcribe audio bytes to text using Whisper (non-blocking)."""
    suffix = os.path.splitext(filename)[1] or ".wav"
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _transcribe_sync, audio_bytes, suffix)
