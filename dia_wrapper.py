# dia_wrapper.py

import subprocess
import os
import sys

# Importera setup-funktion om vi behöver installera Dia
def ensure_dia_ready():
    if not os.path.isdir("dia_tts"):
        print("🛠 Dia not found, running setup...")
        try:
            import setup_dia
            setup_dia.setup_dia()
        except Exception as e:
            print("❌ Failed to set up Dia:", e)
            sys.exit(1)

# Genererar ljud med Dia baserat på text
def generate_audio(text, output_filename):
    ensure_dia_ready()

    script = f"[S1] {text}"
    script_path = os.path.join("dia_tts", "dialog.txt")
    output_path = os.path.abspath(output_filename)

    # Spara texten till fil
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)

    # Kör Dia via CLI
    try:
        subprocess.run([
            "python", "app.py",
            "--script", "dialog.txt",
            "--output", output_filename
        ], cwd="dia_tts", check=True)
    except subprocess.CalledProcessError as e:
        print("❌ Failed to run Dia:", e)
        raise
