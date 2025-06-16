import os
import subprocess
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(PROJECT_ROOT, ".venv")
REQUIREMENTS = os.path.join(PROJECT_ROOT, "requirements.txt")

def run(cmd, shell=False):
    print(f"> {cmd}")
    result = subprocess.run(cmd, shell=shell)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)

def recreate_venv():
    print("Creating new .venv (if not exists)...")
    run([sys.executable, "-m", "venv", ".venv"])

def install_requirements():
    if os.path.exists(REQUIREMENTS):
        print("Installing dependencies from requirements.txt...")
        run([os.path.join(VENV_DIR, "Scripts" if os.name == "nt" else "bin", "python"), "-m", "pip", "install", "-r", REQUIREMENTS])
    else:
        print("⚠️ requirements.txt not found. Skipping package install.")

if __name__ == "__main__":
    recreate_venv()
    install_requirements()
