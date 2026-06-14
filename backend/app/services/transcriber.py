import asyncio
import tempfile
import os

_model = None

def _load_model(model_name: str):
    import whisper
    global _model
    if _model is None:
        _model = whisper.load_model(model_name)
    return _model

def _transcribe_sync(audio_bytes: bytes, suffix: str, model_name: str) -> str:
    model = _load_model(model_name)
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        f.write(audio_bytes)
        tmp_path = f.name
    try:
        result = model.transcribe(tmp_path)
        return result["text"].strip()
    finally:
        os.unlink(tmp_path)

async def transcribe_audio(audio_bytes: bytes, filename: str) -> str:
    from app.core.config import settings
    suffix = os.path.splitext(filename)[1] or ".wav"
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, _transcribe_sync, audio_bytes, suffix, settings.whisper_model
    )
