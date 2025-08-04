# setup_dia.py

import os
import subprocess
import sys
import shutil
import urllib.request

DIA_DIR = "dia_tts"
MODEL_URL = "https://huggingface.co/nari-labs/dia/resolve/main/dia-model.pth"
MODEL_FILE = os.path.join(DIA_DIR, "weights", "dia-model.pth")

# Klonar Dia från GitHub om den inte redan finns
def clone_dia():
    if os.path.exists(DIA_DIR):
        print("✅ Dia already cloned.")
        return
    print("📥 Cloning Dia from GitHub...")
    subprocess.run(["git", "clone", "https://github.com/nari-labs/dia.git", DIA_DIR], check=True)

# Installerar nödvändiga Python-paket direkt (ingen requirements.txt behövs)
def install_dependencies():
    print("📦 Installing Dia dependencies manually...")
    pip_packages = [
        "torch",            # PyTorch
        "torchaudio",       # Ljudstöd
        "transformers",     # Modellhantering
        "einops",           # Tensor-transformationer
        "librosa",          # Audiohantering
        "soundfile",        # Ljudfilshantering
        "scipy",            # Signalbearbetning
        "accelerate"        # Hugging Face optimering
    ]
    subprocess.run([sys.executable, "-m", "pip", "install"] + pip_packages, check=True)

# Laddar ner Dia-modellen om den inte finns
def download_model():
    if os.path.exists(MODEL_FILE):
        print("✅ Dia model already exists.")
        return

    print("🌐 Downloading Dia model weights (~6 GB)...")
    os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)

    try:
        urllib.request.urlretrieve(MODEL_URL, MODEL_FILE)
        print("✅ Model downloaded.")
    except Exception as e:
        print("❌ Failed to download Dia model.")
        print("📌 You may need to log in to Hugging Face CLI or download manually from:")
        print("👉", MODEL_URL)
        raise e

# Kör hela setup-processen
def setup_dia():
    clone_dia()
    install_dependencies()
    download_model()
    print("🎤 Dia setup complete.")

if __name__ == "__main__":
    try:
        setup_dia()
    except Exception as e:
        print("❌ Setup failed:", e)
