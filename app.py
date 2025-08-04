# app.py

import subprocess
import shutil

# Kolla om ollama är installerat
if shutil.which("ollama") is None:
    raise RuntimeError("❌ Ollama is not installed or not in PATH. Install it from https://ollama.com")

# Kolla vilka modeller som är tillgängliga lokalt
def get_local_ollama_models():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        return [line.split()[0] for line in result.stdout.strip().split("\n")[1:] if line]
    except Exception as e:
        print("⚠️ Failed to query Ollama:", e)
        return []

# Använd i /talk endpoint:
if selected_model not in get_local_ollama_models():
    return {"error": f"Model '{selected_model}' not found in Ollama. Please pull it first."}
