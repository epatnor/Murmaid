# setup_dia.py

import os
import subprocess
import sys
from pathlib import Path
from huggingface_hub import hf_hub_download

DIA_DIR = Path("dia_tts")
MODEL_NAME = "dia-model.pth"
MODEL_FILE = DIA_DIR / "weights" / MODEL_NAME

# Klonar Dia från Hugging Face repo om den inte redan finns
def clone_dia():
    if DIA_DIR.exists():
        print("✅ Dia already cloned.")
        return
    print("📥 Cloning Dia from Hugging Face...")
    subprocess.run(["git", "clone", "git@huggingface.co:nari-labs/dia.git", str(DIA_DIR)], check=True)

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

# Laddar ner modellen via huggingface_hub med autentisering
def download_model():
    if MODEL_FILE.exists():
        print("✅ Dia model already exists.")
        return

    print("🌐 Downloading Dia model weights (~6 GB)...")
    try:
        # Hämta till DIA_DIR/weights utan symlink
        model_path = hf_hub_download(
            repo_id="nari-labs/dia",
            filename=MODEL_NAME,
            local_dir=str(DIA_DIR / "weights"),
            local_dir_use_symlinks=False
        )
        print(f"✅ Model downloaded to: {model_path}")
    except Exception as e:
        print("❌ Failed to download Dia model.")
        print("📌 You may need to run `huggingface-cli login` or add SSH access.")
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
