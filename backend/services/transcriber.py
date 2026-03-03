import whisper

_model = None

def get_model():
    global _model
    if _model is None:
        print("Carregando modelo Whisper...")
        _model = whisper.load_model("small")
        print("Modelo Whisper carregado :)")
    return _model

def transcribe_audio(audio_path: str) -> str:
    model = get_model()
    result = model.transcribe(audio_path, fp16=False)
    transcription = result["text"].strip()
    print(f"Transcrição: {transcription}")
    return transcription