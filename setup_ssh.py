# setup_ssh.py

import os
import subprocess
from pathlib import Path

# Define SSH paths
ssh_dir = Path.home() / ".ssh"
ssh_key = ssh_dir / "hf_ed25519"
ssh_config = ssh_dir / "config"

# Create .ssh directory if it doesn't exist
ssh_dir.mkdir(parents=True, exist_ok=True)

# Hugging Face SSH config block
huggingface_config = """
Host huggingface.co
    HostName huggingface.co
    User git
    IdentityFile ~/.ssh/hf_ed25519
    IdentitiesOnly yes
"""

# Write or append to config
if ssh_config.exists():
    with ssh_config.open("r", encoding="utf-8") as f:
        contents = f.read()
    if "Host huggingface.co" not in contents:
        with ssh_config.open("a", encoding="utf-8") as f:
            f.write("\n" + huggingface_config.strip() + "\n")
        print("✅ Hugging Face entry added to .ssh/config.")
    else:
        print("ℹ️ Hugging Face already present in .ssh/config.")
else:
    with ssh_config.open("w", encoding="utf-8") as f:
        f.write(huggingface_config.strip() + "\n")
    print("✅ Created new .ssh/config with Hugging Face entry.")

# Set permissions (important on Unix-like systems)
try:
    os.chmod(ssh_key, 0o600)
    os.chmod(ssh_config, 0o600)
except PermissionError:
    print("⚠️ Could not set permissions (likely ignored on Windows).")

# Test the SSH connection (auto-accepts fingerprint)
print("\n🚀 Testing SSH connection to Hugging Face...")
try:
    result = subprocess.run(
        ["ssh", "-o", "StrictHostKeyChecking=no", "-T", "git@huggingface.co"],
        capture_output=True, text=True
    )
    print(result.stdout.strip())
    print(result.stderr.strip())
except Exception as e:
    print(f"❌ SSH test failed: {e}")

# Reminder to upload public key if not done
print("\n📌 Remember to upload your **public** key to:")
print("   🔗 https://huggingface.co/settings/keys")
print(f"   (your key is at: {ssh_key.with_suffix('.pub')})")
