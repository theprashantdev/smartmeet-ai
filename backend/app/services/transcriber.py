import whisper
import tempfile
import os
from app.core.config import settings

_model = None

def get_model():
    global _model
    if _model is None:
        _model = whisper.load_model(settings.whisper_model)
    return _model

async def transcribe_audio(audio_bytes: bytes, filename: str) -> str:
    """Transcribe audio bytes to text using Whisper."""
    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(filename)[1], delete=False) as f:
        f.write(audio_bytes)
        tmp_path = f.name
    try:
        model = get_model()
        result = model.transcribe(tmp_path)
        return result["text"].strip()
    finally:
        os.unlink(tmp_path)
