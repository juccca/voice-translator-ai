## Pré-requisitos 
- Python 3.11
- FFmpeg instalado e no PATH ([instruções](https://www.gyan.dev/ffmpeg/builds/))

# 1. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar a chave
# edite o arquivo .env e coloque sua GROQ_API_KEY

# 4. Rodar o servidor
cd backend
python -m uvicorn main:app --reload
# Acesse: http://localhost:8000

