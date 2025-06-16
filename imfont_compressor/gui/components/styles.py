import tkinter as tk
import imfont_compressor.core.events as events
from imfont_compressor.core.ui_theme import ColorKeys

def create_separator_row(app, parent_frame, row_index: int):
    parent_frame.grid_columnconfigure(0, weight=1)

    separator = tk.Frame(parent_frame, height=2)
    separator.grid(row=row_index, column=0, padx=app.pad_x, pady=(app.pad_y, 0), sticky="ew")

    app.ui_theme.set_theme_color(separator, bg=ColorKeys.SEPARATOR)
    app.ui_theme.refresh_colors()
    
    return separator

def create_rounded_frame(parent, width=200, height=100, radius=15, bg="#333333"):
    canvas = tk.Canvas(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
    canvas.pack()

    x0, y0, x1, y1 = 0, 0, width, height
    canvas.create_arc(x0, y0, x0+2*radius, y0+2*radius, start=90, extent=90, fill=bg, outline=bg)
    canvas.create_arc(x1-2*radius, y0, x1, y0+2*radius, start=0, extent=90, fill=bg, outline=bg)
    canvas.create_arc(x0, y1-2*radius, x0+2*radius, y1, start=180, extent=90, fill=bg, outline=bg)
    canvas.create_arc(x1-2*radius, y1-2*radius, x1, y1, start=270, extent=90, fill=bg, outline=bg)
    canvas.create_rectangle(x0+radius, y0, x1-radius, y1, fill=bg, outline=bg)
    canvas.create_rectangle(x0, y0+radius, x1, y1-radius, fill=bg, outline=bg)

    inner_frame = tk.Frame(canvas, bg=bg)
    canvas.create_window((width//2, height//2), window=inner_frame, anchor="center")

    return inner_frame

def configure_checkbuttons(app, parent, options):
    for i, (text, var) in enumerate(options):
        cb = tk.Checkbutton(
            parent,
            text=text,
            variable=var,
            command=lambda: events.on_option_changed(app)
        )

        app.ui_theme.set_theme_color(cb, 
           bg=ColorKeys.CHECK_BG,                       
           fg=ColorKeys.CHECK_FG,                     
           activebackground=ColorKeys.CHECK_ACTIVE_BG,                       
           activeforeground=ColorKeys.CHECK_ACTIVE_FG,                   
           selectcolor=ColorKeys.CHECK_SELECTED,                      
        )
        cb.grid(row=1, column=i, sticky="ew")
    app.ui_theme.refresh_colors()