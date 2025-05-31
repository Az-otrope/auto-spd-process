import os
import subprocess
from pathlib import Path
import certifi

# Settings
venv_dir = Path("venv")
cert_file = Path("zscaler_root.pem")

# Step 1: Create virtual environment
print("🔧 Creating virtual environment...")
subprocess.run(["python", "-m", "venv", str(venv_dir)], check=True)

# Step 2: Define paths to pip/python
scripts_dir = venv_dir / "Scripts"
python_exe = scripts_dir / "python.exe"
pip_exe = scripts_dir / "pip.exe"

# Step 3: Install dependencies
print("📦 Installing packages...")
subprocess.run([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"], check=True)
subprocess.run([str(pip_exe), "install", "openai", "requests", "python-dotenv", "certifi"], check=True)

# Step 4: Patch certifi's cacert.pem with Zscaler cert
cacert_path = Path(certifi.where())
print(f"🔐 Patching certifi store at: {cacert_path}")

if cert_file.exists():
    with open(cert_file, "r") as zfile:
        custom_cert = zfile.read()

    with open(cacert_path, "a") as cafile:
        cafile.write("\n" + custom_cert)
    print("✅ Zscaler cert successfully appended.")
else:
    print("❌ Could not find 'zscaler_root.pem' in this folder.")

# Done!
print("\n✅ Virtual environment is ready.")
print(f"👉 To activate it, run:\n{scripts_dir}\\activate")
