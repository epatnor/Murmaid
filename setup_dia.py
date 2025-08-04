# setup_dia.py

import os
import subprocess
import sys
import shutil
import zipfile
import urllib.request

# Huvudkatalog där Dia ska läggas
DIA_DIR = "dia_tts"
DIA_REPO_URL = "https://github.com/nari-labs/dia.git"

# Klonar Dia om det inte finns
def clone_dia():
    if os.path.exists(DIA_DIR):
        print("✅ Dia already cloned.")
        return
    print("📥 Cloning Dia from GitHub...")
    subprocess.run(["git", "clone", DIA_REPO_URL, DIA_DIR], check=True)

# Installerar beroenden med pip (via requirements.txt)
def install_requirements():
    req_path = os.path.join(DIA_DIR, "requirements.txt")
    if not os.path.exists(req_path):
        print("⚠️ No requirements.txt found in Dia directory.")
        return
    print("📦 Installing Dia dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_path], check=True)

# Laddar ner modellen om den inte finns
def download_model():
    weights_dir = os.path.join(DIA_DIR, "weights")
    model_file = os.path.join(weights_dir, "dia-model.pth")

    if os.path.exists(model_file):
        print("✅ Dia model already exists.")
        return

    print("🌐 Downloading Dia model weights (~6 GB)...")
    os.makedirs(weights_dir, exist_ok=True)
    url = "https://huggingface.co/nari-labs/dia/resolve/main/dia-model.pth"
    urllib.request.urlretrieve(url, model_file)
    print("✅ Model downloaded.")

# Kör hela setup-processen
def setup_dia():
    clone_dia()
    install_requirements()
    download_model()
    print("🎤 Dia setup complete.")

if __name__ == "__main__":
    try:
        setup_dia()
    except Exception as e:
        print("❌ Setup failed:", e)
