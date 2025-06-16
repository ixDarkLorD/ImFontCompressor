import tkinter as tk
from imfont_compressor.core.ui_theme import ColorKeys

def styled_button(app, parent, text, command, **kwargs):
    """Create a styled button with consistent appearance."""
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        **kwargs
    )

    app.ui_theme.set_theme_color(btn, 
        bg=ColorKeys.BUTTON_BG,
        fg=ColorKeys.BUTTON_FG,
        disabled_bg=ColorKeys.BUTTON_DISABLED_BG,
        disabled_fg=ColorKeys.BUTTON_DISABLED_FG,
        activebackground=ColorKeys.BUTTON_PRESSED_BG,
        activeforeground=ColorKeys.BUTTON_PRESSED_FG,
    )

    if btn['state'] == "disabled":
        cursor = "arrow"
    else:
        cursor = "hand2"

    btn.configure(cursor=cursor)
    return btn