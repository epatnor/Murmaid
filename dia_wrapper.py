# dia_wrapper.py

import subprocess

# Genererar ljud med Dia baserat på text
def generate_audio(text, output_filename):
    script = f"[S1] {text}"

    # Spara texten till fil som Dia kan läsa
    with open("dialog.txt", "w", encoding="utf-8") as f:
        f.write(script)

    # Kör Dia via CLI (justera om du har annat körsätt)
    try:
        subprocess.run([
            "python", "app.py",
            "--script", "dialog.txt",
            "--output", output_filename
        ], check=True)
    except subprocess.CalledProcessError as e:
        print("❌ Failed to run Dia:", e)
