import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

from imfont_compressor import CURRENT_VERSION
import PyInstaller.__main__

PATH = "imfont_compressor"
ICON_PATH = f"{PATH}/assets/icon.ico"
EXE_NAME = f"{PATH}.exe"

PyInstaller.__main__.run([
    f"{PATH}/main.py",
    "--onefile",
    "--noconsole",
    "--name", EXE_NAME,
    f"--icon={ICON_PATH}",
    "--add-data", f"{PATH}/assets/icon.ico;assets",
    "--add-data", f"{PATH}/assets/logo.png;assets",
    "--add-data", f"{PATH}/assets/themes;assets/themes",
    "--add-data", f"{PATH}/assets/languages;assets/languages",
    "--add-binary", f"{PATH}/data/binary_to_compressed_c.exe;data",
])

