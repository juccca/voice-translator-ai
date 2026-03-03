import os
os.environ["PATH"] += r";C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin"
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import tempfile, os
from services.transcriber import transcribe_audio
from services.translator import translate_text
from services.speaker import generate_speech

app = FastAPI(title="VoiceBridge API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.post("/translate")
async def translate(
    audio: UploadFile = File(...),
    target_language: str = Form(...)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        content = await audio.read()
        tmp.write(content)
        tmp_path = tmp.name
    try:
        transcription = transcribe_audio(tmp_path)
        translation = translate_text(transcription, target_language)
        lang_code = {"english": "en", "mandarin": "zh-TW"}.get(target_language, "en")
        audio_path = generate_speech(translation, lang_code)
        return {
            "transcription": transcription,
            "translation": translation,
            "audio_url": f"/audio/{os.path.basename(audio_path)}"
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.unlink(tmp_path)

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    audio_path = os.path.join(tempfile.gettempdir(), filename)
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Áudio não encontrado")
    return FileResponse(audio_path, media_type="audio/mpeg")

@app.get("/health")
async def health():
    return {"status": "ok"}