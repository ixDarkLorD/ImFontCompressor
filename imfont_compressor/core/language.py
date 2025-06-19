import os
import json
from enum import Enum
from collections import Counter
from imfont_compressor.core.utils import get_resource_path


class TextAlignment(Enum):
    LTR = "ltr"
    RTL = "rtl"

    @staticmethod
    def from_string(value: str):
        if not value:
            return TextAlignment.LTR
        value = value.strip().lower()
        return TextAlignment.RTL if value == "rtl" else TextAlignment.LTR

    def to_justify(self) -> str:
        return "left" if self == TextAlignment.LTR else "right"

    def to_anchor(self) -> str:
        return "w" if self == TextAlignment.LTR else "e"


class Component:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"Component(key={self.key!r}, value={self.value!r})"


class Language:
    fallback_language = None

    def __init__(self, app, lang_code="en_us", localization_dir=None):
        self.app = app
        self.lang_code = lang_code
        self.localization_dir = localization_dir or get_resource_path("assets", "languages")
        self.translations = {}
        self.language_name = ""
        self.alignment = TextAlignment.LTR
        self.load_language(self.lang_code, True)

    def load_language(self, lang_code, ignore=False):
        path = os.path.join(self.localization_dir, f"{lang_code}.json")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"[Localization] Language file not found: {path}")

        duplicates = check_duplicate_keys(path)
        if duplicates:
            raise ValueError(f"[Localization] Duplicate translation keys found in '{lang_code}.json': {duplicates}")

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if lang_code == "en_us":
                Language.fallback_language = data.get("translations", {})

            self.language_name = data.get("name", lang_code)
            self.translations = data.get("translations", {})
            self.alignment = TextAlignment.from_string(data.get("alignment", "ltr"))

            if not ignore:
                print(f"[Localization] Loaded language: {self.language_name} ({lang_code})")

        except Exception as e:
            print(f"[Localization] Failed to load language file: {e}")
            self.translations = {}
            self.language_name = ""
            self.alignment = TextAlignment.LTR

    def get(self, key: str, *args) -> Component:
        if not isinstance(key, str):
            raise TypeError("get() expects a string key")

        fallback_text = f"[{key}]"
        raw_value = self.translations.get(key)

        if raw_value is None and Language.fallback_language:
            raw_value = Language.fallback_language.get(key)

        if raw_value is None:
            raw_value = fallback_text

        try:
            formatted_args = [str(a) if isinstance(a, Component) else a for a in args]

            if '%' in raw_value:
                if len(formatted_args) == 1:
                    raw_value = raw_value % formatted_args[0]
                else:
                    raw_value = raw_value % tuple(formatted_args)

        except Exception:
            pass

        return raw_value

    def set_language(self, lang_code, ignore=False):
        self.lang_code = lang_code
        self.load_language(lang_code, ignore)

    def get_available_languages(self):
        langs = []
        for filename in os.listdir(self.localization_dir):
            if filename.endswith(".json"):
                lang_code = filename[:-5]
                path = os.path.join(self.localization_dir, filename)
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        data = json.load(file)
                        name = data.get("name", lang_code)
                        langs.append((lang_code, name))
                except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
                    print(f"[Language] Skipping invalid language file: {path} ({e})")
                    langs.append((lang_code, lang_code))
        return langs

    def get_language_name(self):
        return self.language_name

    def get_alignment(self) -> TextAlignment:
        return self.alignment


# Utility to check duplicate keys inside "translations"
def check_duplicate_keys(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    keys = []
    inside_translations = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('"translations"'):
            inside_translations = True
        elif inside_translations and stripped.startswith('}'):
            break
        elif inside_translations and ":" in stripped:
            key_part = stripped.split(":", 1)[0].strip()
            if key_part.startswith('"') and key_part.endswith('"'):
                keys.append(key_part.strip('"'))

    duplicates = [key for key, count in Counter(keys).items() if count > 1]
    return duplicates
