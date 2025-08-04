# dia_wrapper.py

import subprocess
import os
import sys

# Importerar och kör setup om Dia inte finns
def ensure_dia_ready():
    if not os.path.isdir("dia_tts"):
        print("🔧 Dia not found. Starting first-time setup...")
        try:
            import setup_dia
            setup_dia.setup_dia()
        except Exception as e:
            print(f"❌ Dia setup failed: {e}")
            sys.exit(1)
    else:
        print("✅ Dia is ready.")

# Genererar ljud från text via Dia
def generate_audio(text, output_filename):
    ensure_dia_ready()

    script = f"[S1] {text}"
    script_path = os.path.join("dia_tts", "dialog.txt")
    output_path = os.path.abspath(output_filename)

    print(f"📝 Writing dialog to {script_path}")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)

    print("🗣️ Running Dia inference...")
    try:
        subprocess.run([
            "python", "app.py",
            "--script", "dialog.txt",
            "--output", output_filename
        ], cwd="dia_tts", check=True)
        print(f"✅ Audio generated: {output_path}")
    except subprocess.CalledProcessError as e:
        print("❌ Dia execution failed:", e)
        raise
