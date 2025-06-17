import json
import os
from typing import TYPE_CHECKING
from imfont_compressor.core.utils import get_encoding_key, get_valid_symbol_name

if TYPE_CHECKING:
    from imfont_compressor.core.app import ImFontCompressorApp  # Only used for type hints

CONFIG_FILE = "user_config.json"

def save_config(app: "ImFontCompressorApp"):
    prefs = {
        "lang": app.language.lang_code,
        "theme": app.ui_theme.theme_name,
        "symbol_name": app.symbol_name_input.get(),
        "encoding": app.var_encoding.get(),
        "disable_compression": app.var_nocompress.get(),
        "no_static": app.var_nostatic.get(),
        "header_output": app.var_header.get()
    }
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(prefs, f, indent=2)
    except Exception as e:
        print(f"Failed to save preferences: {e}")

def load_config(app: "ImFontCompressorApp", ignore=False):
    if os.path.isfile(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                prefs = json.load(f)

            # Load language before anything UI-related
            lang_code = prefs.get("lang")
            if lang_code:
                app.language.set_language(lang_code, ignore)

            # Load theme
            theme_name = prefs.get("theme", "")
            if theme_name:
                if "@" in theme_name:
                    theme_id, version = theme_name.split("@", 1)
                else:
                    theme_id, version = theme_name, None
                app.ui_theme.load_theme(theme_id, version)

            # Load other preferences
            symbol_name = get_valid_symbol_name(prefs.get("symbol_name"))
            app.symbol_name_input.delete(0, "end")
            app.symbol_name_input.insert(0, symbol_name)

            encoding_key = get_encoding_key(prefs.get("encoding"))
            app.var_encoding.set(encoding_key)
            app.var_nocompress.set(prefs.get("disable_compression", False))
            app.var_nostatic.set(prefs.get("no_static", False))
            app.var_header.set(prefs.get("header_output", False))

        except Exception as e:
            if not ignore:
                print(f"Failed to load preferences: {e}")

