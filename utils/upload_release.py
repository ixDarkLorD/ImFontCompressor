import os
import sys
import argparse
import requests
import zipfile
import tempfile
import json
import re

PROJECT_ROOT = os.path.abspath(".")
sys.path.insert(0, PROJECT_ROOT)

try:
    from imfont_compressor import CURRENT_VERSION, RELEASE_TYPE, RELEASE_API
except ImportError:
    print("[!] Failed to import imfont_compressor module. Make sure you run this script from the project root.")
    sys.exit(1)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
EXE_PATH = os.path.join(PROJECT_ROOT, "dist", "imfont_compressor.exe")
CHANGELOG_PATH = os.path.join(PROJECT_ROOT, "CHANGELOG.md")

def extract_changelog(tag: str) -> str:
    if not os.path.isfile(CHANGELOG_PATH):
        return f"Release {tag}\n\n(Changelog file not found)"
    
    with open(CHANGELOG_PATH, encoding="utf-8") as f:
        content = f.read()

    pattern = rf"##\s+\[{re.escape(tag)}\](.*?)(##\s+\[|$)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()

    return f"No changelog entry for {tag}"

def create_release(tag, name, notes, release_type):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    is_prerelease = release_type.lower() in ("beta", "alpha", "preview")
    is_draft = release_type.lower() == "draft"

    data = {
        "tag_name": tag,
        "name": name,
        "body": notes,
        "draft": is_draft,
        "prerelease": is_prerelease
    }

    response = requests.post(RELEASE_API, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    print(f"[+] Created {release_type} release: {tag}")
    return response.json()

def upload_asset(upload_url, file_path):
    filename = os.path.basename(file_path)
    upload_url = upload_url.replace("{?name,label}", f"?name={filename}")
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/octet-stream"
    }
    with open(file_path, "rb") as f:
        response = requests.post(upload_url, headers=headers, data=f.read())
        response.raise_for_status()
        print(f"[✓] Uploaded: {filename}")

def main():
    parser = argparse.ArgumentParser(description="Upload a release with assets to GitHub.")

    parser.add_argument("--version", help="Version tag for release (e.g. v1.2.0)")
    parser.add_argument("--release-type", choices=["release", "beta", "alpha", "draft"], help="Release type")
    parser.add_argument("--notes", help="Release notes (fallback to changelog)")

    args = parser.parse_args()

    versionTag = args.version or CURRENT_VERSION
    release_type = args.release_type or RELEASE_TYPE

    if not versionTag:
        print("[!] Version tag must be specified either via --version or in imfont_compressor.__version__")
        sys.exit(1)

    name = f"v{versionTag}"

    if not GITHUB_TOKEN:
        print("[!] GITHUB_TOKEN environment variable is not set.")
        sys.exit(1)

    if not os.path.isfile(EXE_PATH):
        print(f"[!] Executable not found at: {EXE_PATH}")
        sys.exit(1)

    release_notes = args.notes or extract_changelog(versionTag)

    release = create_release(versionTag, name, release_notes, release_type)
    upload_url = release["upload_url"]
    upload_asset(upload_url, EXE_PATH)

if __name__ == "__main__":
    main()