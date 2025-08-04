# setup_ssh.py

import os
import subprocess
from pathlib import Path

# Kommentar: Definiera sökvägar
ssh_dir = Path.home() / ".ssh"
ssh_key = ssh_dir / "hf_ed25519"
ssh_config = ssh_dir / "config"

# Kommentar: Skapa .ssh-mappen om den inte finns
ssh_dir.mkdir(parents=True, exist_ok=True)

# Kommentar: Skriv SSH-konfiguration för Hugging Face
huggingface_config = """
Host huggingface.co
    HostName huggingface.co
    User git
    IdentityFile ~/.ssh/hf_ed25519
    IdentitiesOnly yes
"""

# Kommentar: Lägg till config (eller uppdatera om det redan finns)
if ssh_config.exists():
    with ssh_config.open("r", encoding="utf-8") as f:
        contents = f.read()
    if "Host huggingface.co" not in contents:
        with ssh_config.open("a", encoding="utf-8") as f:
            f.write("\n" + huggingface_config.strip() + "\n")
        print("✅ Hugging Face konfig tillagd i .ssh/config.")
    else:
        print("ℹ️ Hugging Face finns redan i .ssh/config.")
else:
    with ssh_config.open("w", encoding="utf-8") as f:
        f.write(huggingface_config.strip() + "\n")
    print("✅ Skapade ny .ssh/config med Hugging Face-inställningar.")

# Kommentar: Sätt rätt rättigheter (särskilt viktigt på Linux/macOS)
try:
    os.chmod(ssh_key, 0o600)
    os.chmod(ssh_config, 0o600)
except PermissionError:
    print("⚠️ Kunde inte sätta filrättigheter (ignorerar på Windows).")

# Kommentar: Testa anslutningen (visar om SSH fungerar)
print("\n🚀 Testar SSH-anslutning till Hugging Face...")
try:
    result = subprocess.run(["ssh", "-T", "git@huggingface.co"], capture_output=True, text=True)
    print(result.stdout.strip())
    print(result.stderr.strip())
except Exception as e:
    print(f"❌ Kunde inte testa SSH: {e}")

# Kommentar: Tips om att lägga till nyckeln om det krävs
print("\n📌 Kom ihåg att lägga till din **publika** nyckel på:")
print("   🔗 https://huggingface.co/settings/tokens")
print(f"   (nyckel finns i: {ssh_key.with_suffix('.pub')})")
