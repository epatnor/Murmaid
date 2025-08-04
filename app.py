# app.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess
import uuid
import shutil
import os

from dia_wrapper import generate_audio

# 🚀 Start FastAPI
app = FastAPI()

# 🔧 Static & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ✅ Kontrollera att Ollama finns
if shutil.which("ollama") is None:
    raise RuntimeError("❌ Ollama is not installed or not in PATH. Install it from https://ollama.com")

# 📦 Hämta lokalt installerade Ollama-modeller
def get_local_ollama_models():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        models = []
        for line in result.stdout.strip().split("\n")[1:]:
            if line:
                model = line.split()[0]
                models.append(model)
        return models
    except Exception as e:
        print("⚠️ Failed to query Ollama:", e)
        return []

# 🌐 Root-endpoint – laddar UI med lista över modeller
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    models = get_local_ollama_models()
    return templates.TemplateResponse("index.html", {"request": request, "models": models})

# 🤖 Hanterar prompt + TTS-svar
@app.post("/talk")
async def talk(request: Request, prompt: str = Form(...), model: str = Form(...)):
    available_models = get_local_ollama_models()
    if model not in available_models:
        return JSONResponse(
            status_code=400,
            content={"error": f"Model '{model}' is not available locally. Please run: ollama pull {model}"}
        )

    # 🧠 Skicka prompt till vald Ollama-modell
    try:
        import ollama
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        if isinstance(response, dict) and "message" in response:
            reply_text = response["message"]["content"]
        else:
            return JSONResponse(status_code=500, content={"error": f"Invalid response from Ollama: {response}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Ollama error: {str(e)}"})

    # 🔊 Generera ljud via Dia
    filename = f"audio_{uuid.uuid4().hex}.wav"
    generate_audio(reply_text, filename)

    return {"text": reply_text, "audio_url": f"/audio/{filename}"}

# 🎧 Endpoint för ljuduppspelning
@app.get("/audio/{filename}")
async def get_audio(filename: str):
    filepath = os.path.join(".", filename)
    if not os.path.isfile(filepath):
        return JSONResponse(status_code=404, content={"error": "File not found."})
    return FileResponse(filepath, media_type="audio/wav")
