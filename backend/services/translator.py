import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

LANGUAGE_NAMES = {
    "english": "inglês",
    "mandarin": "mandarim (chinês simplificado)"
}

def translate_text(text: str, target_language: str) -> str:
    lang_name = LANGUAGE_NAMES.get(target_language, target_language)

    prompt = (
        f"Você é um tradutor profissional. "
        f"Traduza o texto abaixo para {lang_name}. "
        f"Responda APENAS com a tradução, sem explicações, sem aspas, sem comentários.\n\n"
        f"Texto: {text}"
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    translation = response.choices[0].message.content.strip()
    print(f"Tradução ({lang_name}): {translation}")
    return translation