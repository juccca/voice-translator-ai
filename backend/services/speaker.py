import tempfile
import os
from gtts import gTTS

def generate_speech(text: str, lang_code: str) -> str:
    tts = gTTS(text=text, lang=lang_code, slow=False)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", dir=tempfile.gettempdir())
    tts.save(tmp.name)
    print(f"Áudio gerado: {tmp.name}")
    return tmp.name