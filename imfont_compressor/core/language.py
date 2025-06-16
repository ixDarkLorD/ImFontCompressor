import os
import json
from collections import Counter
from imfont_compressor.core.utils import get_resource_path

class Component:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"Component(key={self.key!r}, value={self.value!r})"

    def format(self, *args):
        try:
            if args:
                formatted_value = self.value % args if len(args) > 1 else self.value % args[0]
            else:
                formatted_value = self.value
            return Component(self.key, formatted_value)
        except Exception as e:
            print(f"[Component] Formatting error for key '{self.key}': {e}")
            return self

class Language:
    def __init__(self, app, lang_code="en_us", localization_dir=None):
        self.app = app
        self.lang_code = lang_code
        self.localization_dir = localization_dir or get_resource_path("assets", "languages")
        self.translations = {}
        self.language_name = ""
        self.load_language(self.lang_code)

    def load_language(self, lang_code):
        path = os.path.join(self.localization_dir, f"{lang_code}.json")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"[Localization] Language file not found: {path}")

        duplicates = check_duplicate_keys(path)
        if duplicates:
            raise ValueError(f"[Localization] Duplicate translation keys found in '{lang_code}.json': {duplicates}")

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.language_name = data.get("name", lang_code)
            self.translations = data.get("translations", {})
            print(f"[Localization] Loaded language: {self.language_name} ({lang_code})")

        except Exception as e:
            print(f"[Localization] Failed to load language file: {e}")
            self.translations = {}
            self.language_name = ""

    def get(self, key: str, *args) -> Component:
        if not isinstance(key, str):
            raise TypeError("get() expects a string key")

        fallback = f"[{key}]"
        raw_value = self.translations.get(key, fallback)

        if args:
            formatted_args = []
            for a in args:
                if isinstance(a, Component):
                    formatted_args.append(str(a))
                elif isinstance(a, str):
                    formatted_args.append(a)
                else:
                    raise TypeError(f"Formatting arguments must be str or Component, got {type(a)}")

            try:
                raw_value = raw_value % tuple(formatted_args) if len(formatted_args) > 1 else raw_value % formatted_args[0]
            except Exception as e:
                print(f"[Language] Formatting error for key '{key}': {e}")

        return Component(key, raw_value)

    def set_language(self, lang_code):
        self.lang_code = lang_code
        self.load_language(lang_code)

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

# Utils

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
