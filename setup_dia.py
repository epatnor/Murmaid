# setup_dia.py

import os
import subprocess
import sys
import shutil
from huggingface_hub import hf_hub_download

DIA_DIR = "dia_tts"
MODEL_FILENAME = "dia-v0_1.pth"
REPO_ID = "nari-labs/Dia-1.6B"
MODEL_FILE = os.path.join(DIA_DIR, "weights", MODEL_FILENAME)

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
        "torch",
        "torchaudio",
        "transformers",
        "einops",
        "librosa",
        "soundfile",
        "scipy",
        "accelerate",
        "huggingface_hub"
    ]
    subprocess.run([sys.executable, "-m", "pip", "install"] + pip_packages, check=True)

# Laddar ner Dia-modellen via Hugging Face Hub
def download_model():
    if os.path.exists(MODEL_FILE):
        print("✅ Dia model already exists.")
        return

    print("🌐 Downloading Dia model weights (~6 GB)...")
    os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)

    try:
        model_path = hf_hub_download(repo_id=REPO_ID, filename=MODEL_FILENAME)
        shutil.copy(model_path, MODEL_FILE)
        print("✅ Model downloaded and copied to weights folder.")
    except Exception as e:
        print("❌ Failed to download Dia model.")
        print("📌 Make sure you are logged in to Hugging Face CLI.")
        print(f"👉 https://huggingface.co/{REPO_ID}/blob/main/{MODEL_FILENAME}")
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
