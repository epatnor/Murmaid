# app.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess
import uuid
import shutil
from dia_wrapper import generate_audio

# Starta FastAPI och mounta statiska filer
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Kontrollera att Ollama är installerat
if shutil.which("ollama") is None:
    raise RuntimeError("❌ Ollama is not installed or not in PATH. Install it from https://ollama.com")

# Funktion för att hämta listan över lokalt nedladdade modeller
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

# Root-route med modellval i frontend
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    models = get_local_ollama_models()
    return templates.TemplateResponse("index.html", {"request": request, "models": models})

# Endpoint som hanterar prompt och vald modell
@app.post("/talk")
async def talk(request: Request, prompt: str = Form(...), model: str = Form(...)):
    available_models = get_local_ollama_models()
    if model not in available_models:
        return JSONResponse(status_code=400, content={"error": f"Model '{model}' is not available locally. Please pull it first using 'ollama pull {model}'."})

    # Skicka prompt till Ollama
    try:
        import ollama
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        reply_text = response['message']['content']
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Ollama error: {str(e)}"})

    # Generera ljud från svaret
    filename = f"audio_{uuid.uuid4().hex}.wav"
    generate_audio(reply_text, filename)

    return {"text": reply_text, "audio_url": f"/audio/{filename}"}

# Endpoint för att hämta ljudfil
@app.get("/audio/{filename}")
async def get_audio(filename: str):
    return FileResponse(filename, media_type="audio/wav")
