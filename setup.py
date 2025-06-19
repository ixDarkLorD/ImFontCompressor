#!/usr/bin/env python3
"""
Project Setup Script (Multi-Mode)
Handles virtual environment and dependency management with three modes:
1. Basic check (default) - For debug launches
2. Full install (--install) - First-time setup
3. Force rebuild (--force) - Clean environment rebuild
"""

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

# Constants
PROJECT_ROOT = Path(__file__).parent.resolve()
VENV_DIR = PROJECT_ROOT / ".venv"
REQUIREMENTS = PROJECT_ROOT / "requirements.txt"
PYTHON_EXECUTABLE = sys.executable

class SetupManager:
    def __init__(self):
        self.mode = self._detect_mode()
        
    def _detect_mode(self) -> str:
        """Determine setup mode from command line args."""
        if "--force" in sys.argv:
            return "force"
        if "--install" in sys.argv:
            return "install"
        return "basic"

    def run_command(self, cmd: List[str], shell: bool = False) -> None:
        """Execute a command with error handling."""
        print(f"🚀 Running: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True, shell=shell)
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed with exit code {e.returncode}")
            sys.exit(e.returncode)

    def get_venv_python(self) -> Path:
        """Get the correct Python path for the virtual environment."""
        if platform.system() == "Windows":
            return VENV_DIR / "Scripts" / "python.exe"
        return VENV_DIR / "bin" / "python"

    def check_venv(self) -> bool:
        """Check if virtual environment exists and is valid."""
        if not VENV_DIR.exists():
            if self.mode == "basic":
                print("⚠️ No virtual environment found - run with --install for full setup")
                sys.exit(1)
            return False
        return True

    def setup_venv(self) -> None:
        """Handle virtual environment creation based on mode."""
        if self.mode == "force":
            print("🔨 Force-recreating virtual environment...")
            self.run_command([PYTHON_EXECUTABLE, "-m", "venv", "--clear", str(VENV_DIR)])
        elif not VENV_DIR.exists():
            print("🛠️ Creating new virtual environment...")
            self.run_command([PYTHON_EXECUTABLE, "-m", "venv", str(VENV_DIR)])

    def install_dependencies(self) -> None:
        """Install dependencies based on mode."""
        if self.mode == "basic":
            return  # Skip for basic mode
            
        if not REQUIREMENTS.exists():
            print("⚠️ requirements.txt not found - skipping dependencies")
            return

        print("📦 Installing dependencies...")
        venv_python = self.get_venv_python()
        self.run_command([
            str(venv_python), "-m", "pip", "install",
            "--upgrade", "pip", "-r", str(REQUIREMENTS)
        ])

    def show_activation(self) -> None:
        """Show how to activate the virtual environment."""
        if "--activate" not in sys.argv:
            return
            
        print("\nTo activate the virtual environment:")
        if platform.system() == "Windows":
            print(f"  {VENV_DIR}\\Scripts\\activate")
        else:
            print(f"  source {VENV_DIR}/bin/activate")

def main():
    print("\n" + "=" * 50)
    print(f"🚧 Project Setup: {PROJECT_ROOT}")
    print("=" * 50 + "\n")

    manager = SetupManager()
    
    if manager.mode == "basic":
        print("🔍 Running basic environment check...")
        if manager.check_venv():
            print("✅ Virtual environment exists - ready for development")
            sys.exit(0)
    else:
        manager.setup_venv()
        manager.install_dependencies()

    manager.show_activation()
    print("\n" + "=" * 50)
    print(f"✅ {manager.mode.capitalize()} setup completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()