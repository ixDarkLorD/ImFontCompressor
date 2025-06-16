import os
import sys
import tkinter as tk

encoding_map = {
    "Unsigned 8-bit (-u8)": "-u8",
    "Unsigned 32-bit (-u32)": "-u32",
    "Base85 Encoded (-base85)": "-base85"
}

def get_encoding_value(key):
    return encoding_map.get(key, list(encoding_map.values())[0])

def get_encoding_key(value=None):
    if value is not None:
        for k, v in encoding_map.items():
            if v == value:
                return k
    # fallback safely, or raise error if preferred
    if encoding_map:
        return next(iter(encoding_map))
    else:
        raise ValueError("encoding_map is empty, cannot get default key")


def get_valid_symbol_name(name, fallback="example"):
    if isinstance(name, str) and any(c.isalpha() for c in name):
        return name
    return fallback

def get_project_root():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_resource_path(*path_parts):
    """
    Get absolute path to resource, works both when running normally
    or from PyInstaller bundle.

    Example:
        get_resource_path("assets", "themes", "dark.json")
    """
    base_path = get_project_root()
    return os.path.join(base_path, *path_parts)
    
def enable_drag_and_drop(widget, app):
    """
    Enable drag-and-drop file support on a tkinter widget.
    Expects `app` to be an instance of FontCompressorApp with
    members: font_input (Entry), status_label (Label).

    Drops update the font_input Entry and status_label Label.
    """

    from imfont_compressor.core.ui_theme import ColorKeys
    try:
        from tkinterdnd2 import DND_FILES
    except ImportError:
        print("tkinterdnd2 not available — drag and drop disabled.")
        return

    def on_drop(event):
        dropped_files = event.data
        files = [f.strip('{}') for f in dropped_files.split()]
        if not files:
            return
        dropped_file = files[0]

        if os.path.isfile(dropped_file):
            ext = os.path.splitext(dropped_file)[1].lower()
            if ext in [".ttf", ".otf"]:
                # Update font_input Entry
                if app.font_input:
                    app.font_input.delete(0, tk.END)
                    app.font_input.insert(0, dropped_file)
                # Update status_label
                if app.status_label:
                    app.status_label.config(text=app.language.get("main.status").format(app.language.get("main.status.idle")), fg=app.ui_theme.get_color(ColorKeys.STATUS_IDLE))
            else:
                if app.status_label:
                    app.status_label.config(text=app.language.get("main.status").format(app.language.get("main.status.invalid_type_drop")), fg=app.ui_theme.get_color(ColorKeys.STATUS_ERROR))
        else:
            if app.status_label:
                app.status_label.config(text=app.language.get("main.status").format(app.language.get("main.status.invalid_drop")), fg=app.ui_theme.get_color(ColorKeys.STATUS_ERROR))

    widget.drop_target_register(DND_FILES)
    widget.dnd_bind('<<Drop>>', on_drop)
