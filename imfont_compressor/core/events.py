import json
import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser
import threading
import urllib.request
import re
from imfont_compressor.core.config import save_config
from imfont_compressor.core.ui_theme import ColorKeys
from imfont_compressor.core.app import ImFontCompressorApp
from imfont_compressor.core.utils import encoding_map, get_encoding_value
from imfont_compressor import CURRENT_VERSION, DISCORD_URL, RELEASE_API, GITHUB_URL

def on_theme_changed(app: ImFontCompressorApp):
    themes = app.ui_theme.list_available_themes()
    display_to_id_version = {}

    for theme_id, versions in themes.items():
        if len(versions) == 1:
            theme = versions[0]
            name = theme.get("name", theme_id)
            # Map display name to (id, version)
            display_to_id_version[name] = (theme_id, theme.get("version", "1.0"))
        else:
            for theme in versions:
                name = theme.get("name", theme_id)
                version = theme.get("version", "1.0")
                display_name = f"{name} (v{version})"
                display_to_id_version[display_name] = (theme_id, version)

    selected_display = app.theme_combo.get()
    if selected_display not in display_to_id_version:
        print(f"[Theme] Selected theme '{selected_display}' not found in available themes.")
        return

    theme_id, version = display_to_id_version[selected_display]

    try:
        if hasattr(app.ui_theme, "apply_theme_with_version"):
            app.ui_theme.apply_theme_with_version(theme_id, version)
        else:
            app.ui_theme.apply_theme(theme_id)
        save_config(app)
    except Exception as e:
        print(f"[Theme] Failed to apply theme '{theme_id}' version '{version}': {e}")

def on_language_changed(app: ImFontCompressorApp):
    selected_name = app.language_combo.get()

    selected_code = None
    for code, name in app.language.get_available_languages():
        if name == selected_name:
            selected_code = code
            break

    if selected_code is None or selected_code == app.language.lang_code:
        return

    app.language.set_language(selected_code, True)
    save_config(app)

    messagebox.showinfo(
        title=app.language.get("options.message.restart"),
        message=app.language.get("options.message.restart.language")
    )

def browse_font(app: ImFontCompressorApp):
    file = filedialog.askopenfilename(filetypes=[("Font Files", "*.ttf *.otf")])
    if file:
        app.font_input.delete(0, tk.END)
        app.font_input.insert(0, file)
        app.status_label.config(
            text=app.language.get("compressor.status", app.language.get("compressor.status.idle")), 
            fg=app.ui_theme.get_color(ColorKeys.STATUS_IDLE)
        )

def on_option_changed(app: ImFontCompressorApp):
    if not app.initialized:
        return

    app.btn_compress.config(state="normal")
    app.btn_copy.config(state="disabled")
    app.btn_save.config(state="disabled")
    app.status_label.config(
        text=app.language.get("compressor.status", app.language.get("compressor.status.idle")), 
        fg=app.ui_theme.get_color(ColorKeys.STATUS_IDLE)
    )

def compress_font(app: ImFontCompressorApp):
    from imfont_compressor.core.compressor import run_compression
    
    params = {
        "font_path": app.font_input.get().strip(),
        "symbol_name": app.symbol_name_input.get().strip(),
        "encoding": get_encoding_value(app.var_encoding.get()),
        "disable_compression": app.var_nocompress.get(),
        "no_static": app.var_nostatic.get(),
        "header_output": app.var_header.get()
    }

    def status_set(text, fg):
        app.status_label.config(text=text, fg=fg)
        app.root.update_idletasks()

    status_set(app.language.get("compressor.status", app.language.get("compressor.status.compressing")), app.ui_theme.get_color(ColorKeys.STATUS_WARNING))

    result = run_compression(params, status_set)

    if result["success"]:
        app.last_output_text = result["output_text"]
        app.last_output_file = result["output_file"]

        app.btn_copy.config(state="normal")
        app.btn_save.config(state="normal")

        status_set(app.language.get("compressor.status", app.language.get("compressor.status.compressed")), app.ui_theme.get_color(ColorKeys.STATUS_SUCCESS))
        app.ui_theme.refresh_colors()
        save_config(app)
    else:
        status_set(f"({app.language.get("message.error")}) {result['error']}", app.ui_theme.get_color(ColorKeys.STATUS_ERROR))

def copy_result(app: ImFontCompressorApp):
    if app.last_output_text:
        app.root.clipboard_clear()
        app.root.clipboard_append(app.last_output_text)
        messagebox.showinfo(
            app.language.get("compressor.message.copy"),
            app.language.get("compressor.message.copy_compressed_font")
        )

def save_result(app: ImFontCompressorApp):
    if app.last_output_text:
        ext = ".h" if app.var_header.get() else ".cpp"
        filetypes = [("Header File", "*.h")] if ext == ".h" else [("CPP File", "*.cpp")]
        f = filedialog.asksaveasfile(mode='w', defaultextension=ext, filetypes=filetypes)
        if f:
            f.write(app.last_output_text)
            f.close()
            messagebox.showinfo(
                app.language.get("compressor.message.save"), 
                app.language.get("compressor.message.save_compressed_font", f.name)
            )

def reset_to_defaults(app: ImFontCompressorApp):
    app.var_encoding.set(list(encoding_map.keys())[0])
    app.var_nocompress.set(False)
    app.var_nostatic.set(False)
    app.var_header.set(False)
    app.font_input.delete(0, tk.END)
    app.symbol_name_input.delete(0, tk.END)
    app.symbol_name_input.insert(0, "example")
    app.status_label.config(
        text=app.language.get("compressor.status", app.language.get("compressor.status.reset")), 
        fg=app.ui_theme.get_color(ColorKeys.STATUS_SUCCESS)
    )
    save_config(app)

def open_discord(app: ImFontCompressorApp):
    try:
        webbrowser.open(DISCORD_URL)
    except Exception as e:
        messagebox.showerror(
            app.language.get("message.error"), 
            app.language.get("options.message.error.opening_discord", e)
        )

def open_github(app: ImFontCompressorApp):
    try:
        webbrowser.open(GITHUB_URL)
    except Exception as e:
        messagebox.showerror(
            app.language.get("message.error"), 
            app.language.get("options.message.error.opening_github", e)
        )

def compare_versions(v1, v2):
    def parse_version(version):
        return [int(num) for num in re.sub(r'[^0-9.]', '', version).split('.')]
    
    v1_parts = parse_version(v1)
    v2_parts = parse_version(v2)
    
    for i in range(max(len(v1_parts), len(v2_parts))):
        v1_part = v1_parts[i] if i < len(v1_parts) else 0
        v2_part = v2_parts[i] if i < len(v2_parts) else 0
        
        if v1_part < v2_part:
            return -1
        elif v1_part > v2_part:
            return 1
    
    return 0

def get_update_status():
    try:
        with urllib.request.urlopen(RELEASE_API + "/latest") as response:
            data = json.load(response)
            latest_version = data["tag_name"].lstrip("v")
            download_url = data["html_url"]
            
            comparison = compare_versions(CURRENT_VERSION, latest_version)
            is_update = comparison < 0
            
            return {
                "is_update": is_update,
                "latest_version": latest_version,
                "download_url": download_url
            }
    except Exception as e:
        print(f"Error checking for updates: {str(e)}")
        return {
            "is_update": False,
            "latest_version": "",
            "download_url": ""
        }

def get_update_message(app: ImFontCompressorApp, status):
    if status["is_update"]:
        title = app.language.get("options.message.update.available")
        message = app.language.get("options.message.update.ask", status['latest_version'])
        return title, message, True
    else:
        return app.language.get("options.message.update.up_to_date"), app.language.get("options.message.update.latest"), False

def check_and_notify_update(app: ImFontCompressorApp):
    def _check():
        try:
            app.update_btn.configure(state="disabled")
            status = get_update_status()
            title, message, is_update = get_update_message(app, status)
        
            if is_update:
                if messagebox.askyesno(title, message):
                    webbrowser.open(status["download_url"])
            else:
                messagebox.showinfo(title, message)

            app.update_btn.configure(state="normal")

        except Exception as e:
            app.update_btn.configure(state="normal")
            messagebox.showerror(
                app.language.get("message.error"), 
                app.language.get("options.message.error.check_for_updates", str(e))
            )

    threading.Thread(target=_check, daemon=True).start()

def parse_version(version):
    main, *pre = re.sub(r'[^0-9A-Za-z.-]', '', version).split('-', 1)
    parts = [int(num) for num in main.split('.')]
    
    pre_num = 0
    if pre:
        pre_str = pre[0].lower()
        if 'beta' in pre_str:
            pre_num = 1
        elif 'alpha' in pre_str:
            pre_num = 2
        elif 'rc' in pre_str:
            pre_num = 3
    
    return parts + [pre_num]