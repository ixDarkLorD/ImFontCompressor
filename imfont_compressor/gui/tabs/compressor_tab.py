import tkinter as tk
from tkinter import ttk, font as tkfont
from imfont_compressor.gui.components.buttons import styled_button
from imfont_compressor.gui.components.entries import create_entry
from imfont_compressor.gui.components.styles import configure_checkbuttons, create_separator_row
from imfont_compressor.core.utils import encoding_map, enable_drag_and_drop
import imfont_compressor.core.events as events
from imfont_compressor.core.ui_theme import ColorKeys
from imfont_compressor.core.language import TextAlignment
from imfont_compressor.core.app import ImFontCompressorApp

class CompressorTab:
    def __init__(self, app: ImFontCompressorApp, container: ttk.Notebook):
        self.app = app
        self.container = container
        self._create_tab()
        self._setup_file_section()
        self._setup_encoding_section()
        self._setup_extras_section()
        self._setup_action_section()
        self._setup_button_section()

    def _create_tab(self):
        self.frame = tk.Frame(self.container, bd=2, relief="ridge")
        self.container.add(self.frame, text=self.app.language.get("tab.compressor"))

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        
        create_separator_row(self.app, self.frame, 2)
        create_separator_row(self.app, self.frame, 5)
        
        enable_drag_and_drop(self.frame, self.app)

    def _setup_file_section(self):
        align = self.app.language.get_alignment()
        is_ltr = align == TextAlignment.LTR

        frame = tk.Frame(self.frame)
        frame.grid(row=0, column=0, sticky="ew", padx=self.app.pad_x, pady=(self.app.pad_y, 0))
        frame.grid_columnconfigure(0 if is_ltr else 1, weight=1)
        self.app.ui_theme.apply_colors(frame, bg=ColorKeys.BG_CHILD_FRAME)

        label = tk.Label(frame, text=self.app.language.get("compressor.label.font_file"))
        label.grid(row=0, column=0 if is_ltr else 1, sticky="w" if is_ltr else "e", padx=self.app.pad_x, pady=(self.app.pad_y, 0))
        self.app.ui_theme.apply_colors(label, bg=ColorKeys.BG_CHILD_FRAME, fg=ColorKeys.LABEL)

        self.app.font_input = create_entry(frame, justify=align.to_justify())
        self.app.font_input.grid(row=1, column=0 if is_ltr else 1, sticky="ew", padx=(self.app.pad_x, 0) if is_ltr else (0, self.app.pad_x))

        browse_btn = styled_button(
            self.app, frame, f"{self.app.language.get("compressor.button.browse")}",
            lambda: events.browse_font(self.app),
            width=10
        )
        browse_btn.grid(row=1, column=1 if is_ltr else 0, sticky="e" if is_ltr else "w", padx=(self.app.pad_x, self.app.pad_x))

        dnd_frame = tk.Frame(frame)
        dnd_frame.grid(row=2, column=0 if is_ltr else 1, sticky="ew")
        dnd_frame.columnconfigure(0 if is_ltr else 1, weight=1)

        center_frame = tk.Frame(dnd_frame)
        center_frame.pack(anchor="w" if is_ltr else "e")

        # Icon label
        icon_label = tk.Label(
            center_frame,
            text="💡",
            font=tkfont.Font(family="Segoe UI", size=8)
        )
        icon_label.pack(side="left" if is_ltr else "right", padx=(4, 0) if is_ltr else (0, 4))

        # Text label
        text_label = tk.Label(
            center_frame,
            text=str(self.app.language.get("compressor.label.font_file.dnd")),
            font=tkfont.Font(size=8, slant="italic")
        )
        text_label.pack(side="left" if is_ltr else "right")

        self.app.ui_theme.apply_colors(dnd_frame, bg=ColorKeys.BG_CHILD_FRAME)
        self.app.ui_theme.apply_colors(center_frame, bg=ColorKeys.BG_CHILD_FRAME)
        self.app.ui_theme.apply_colors(icon_label, bg=ColorKeys.BG_CHILD_FRAME, fg=ColorKeys.INPUT_INSIDE)
        self.app.ui_theme.apply_colors(text_label, bg=ColorKeys.BG_CHILD_FRAME, fg=ColorKeys.INPUT_INSIDE)

        self._setup_symbol_name_section(frame)

    def _setup_symbol_name_section(self, frame: tk.Frame):
        align = self.app.language.get_alignment()
        is_ltr = align == TextAlignment.LTR

        label = tk.Label(frame, text=f"{self.app.language.get("compressor.label.symbol_name")}")
        label.grid(row=3, column=0 if is_ltr else 1, sticky="w" if is_ltr else "e", pady=(4, 2), padx=self.app.pad_x)
        self.app.ui_theme.apply_colors(label, bg=ColorKeys.BG_CHILD_FRAME, fg=ColorKeys.LABEL)

        self.app.symbol_name_input = create_entry(
            frame,
            width=50,
            bg=self.app.ui_theme.get_color("COLOR_ENTRY_BG"),
            fg=self.app.ui_theme.get_color("COLOR_ENTRY_FG"),
            insertbackground=self.app.ui_theme.get_color("COLOR_ENTRY_INSERT_BG"),
            justify=align.to_justify()
        )

        self.app.symbol_name_input.insert(0, "example")
        self.app.symbol_name_input.grid(
            row=4, column=0,
            columnspan=2,
            sticky="ew", 
            pady=(0, self.app.pad_y + 4), 
            padx=self.app.pad_x
        )

    def _setup_encoding_section(self):
        align = self.app.language.get_alignment()
        is_ltr = align == TextAlignment.LTR

        frame = tk.Frame(self.frame)
        frame.grid(row=3, column=0, sticky="w" if is_ltr else "e", padx=self.app.pad_x, pady=(self.app.pad_y, 0))
        self.app.ui_theme.apply_colors(frame,
            bg=ColorKeys.BG_CHILD_FRAME
        )

        label = tk.Label(frame, text=self.app.language.get("compressor.label.encoding"))
        self.app.ui_theme.apply_colors(label,
            bg=ColorKeys.BG_CHILD_FRAME,
            fg=ColorKeys.LABEL
        )

        combo_width = max(len(k) for k in encoding_map.keys())
        self.app.encoding_combo = ttk.Combobox(
            frame,
            textvariable=self.app.var_encoding,
            width=combo_width,
            state="readonly"
        )
        self.app.encoding_combo['values'] = list(encoding_map.keys())
        self.app.encoding_combo.bind("<<ComboboxSelected>>", events.on_option_changed(self.app))

        label.grid(row=0, column=0 if is_ltr else 1, sticky="w" if is_ltr else "e", padx=(0, 3) if is_ltr else (3, 0))
        self.app.encoding_combo.grid(row=0, column=1 if is_ltr else 0, sticky="w" if is_ltr else "e")

    def _setup_extras_section(self):
        frame = tk.Frame(self.frame)
        frame.grid(row=4, column=0, sticky="ew", pady=0, padx=self.app.pad_x)
        self.app.ui_theme.apply_colors(frame,
            bg=ColorKeys.BG_CHILD_FRAME
        )

        # Get alignment direction
        align = self.app.language.get_alignment()
        is_ltr = align == TextAlignment.LTR

        label = tk.Label(frame, text=self.app.language.get("compressor.label.extras"))
        label.grid(row=0, column=0 if is_ltr else 2, sticky="w" if is_ltr else "e")
        self.app.ui_theme.apply_colors(label,
            bg=ColorKeys.BG_CHILD_FRAME,
            fg=ColorKeys.LABEL
        )

        options = [
            ("Disable Compression", self.app.var_nocompress),
            ("No Static (Do not use 'static')", self.app.var_nostatic),
            ("Output as .h (Header)", self.app.var_header)
        ]

        configure_checkbuttons(
            self.app,
            frame,
            options
        )
        frame.grid_columnconfigure(1, weight=1)

    def _setup_action_section(self):
        frame = tk.Frame(
            self.frame,
            bg=self.app.ui_theme.get_color("COLOR_BG_ACTION_FRAME")
        )
        frame.grid(row=6, column=0, sticky="ew", pady=self.app.pad_y)

        # Create compress button
        self.app.btn_compress = styled_button(
            self.app,
            frame,
            self.app.language.get("compressor.button.compress_font"),
            lambda: events.compress_font(self.app),
            width=18
        )

        # Create status label
        status_text = self.app.language.get("compressor.status", self.app.language.get("compressor.status.idle"))
        self.app.status_label = tk.Label(
            frame,
            text=status_text,
            font=tkfont.Font(size=9, slant="italic")
        )

        # Determine alignment
        align = self.app.language.get_alignment()
        if align == TextAlignment.LTR:
            frame.grid_columnconfigure(1, weight=1)
            self.app.btn_compress.grid(
                row=0, column=0, sticky="ew",
                pady=(self.app.pad_y, 0),
                padx=(self.app.pad_x, 0)
            )
            self.app.status_label.grid(
                row=0, column=1, sticky="ew",
                pady=(self.app.pad_y, 0),
                padx=self.app.pad_x
            )
        else:  # RTL
            frame.grid_columnconfigure(0, weight=1)
            self.app.status_label.grid(
                row=0, column=0, sticky="ew",
                pady=(self.app.pad_y, 0),
                padx=self.app.pad_x
            )
            self.app.btn_compress.grid(
                row=0, column=1, sticky="ew",
                pady=(self.app.pad_y, 0),
                padx=(0, self.app.pad_x)
            )

        # Apply theme colors to status label
        self.app.ui_theme.apply_colors(
            self.app.status_label,
            bg=ColorKeys.BG_CHILD_FRAME,
            fg=ColorKeys.LABEL
        )

    def _setup_button_section(self):
        frame = tk.Frame(
            self.frame,
            bg=self.app.ui_theme.get_color(ColorKeys.BG_CHILD_FRAME)
        )
        frame.grid(row=7, column=0, padx=self.app.pad_x, pady=(self.app.pad_y, self.app.pad_y + 5))
        frame.grid_columnconfigure(0, weight=1)

        btn_reset = styled_button(
            self.app, frame, self.app.language.get("compressor.button.reset"), 
            lambda: events.reset_to_defaults(self.app), 
            padx=12, pady=10, width=18
        )

        self.app.btn_copy = styled_button(
            self.app, frame, self.app.language.get("compressor.button.copy"), 
            lambda: events.copy_result(self.app), 
            padx=12, pady=10, width=18, state="disabled"
        )

        self.app.btn_save = styled_button(
            self.app, frame, self.app.language.get("compressor.button.save"), 
            lambda: events.save_result(self.app), 
            padx=12, pady=10, width=18, state="disabled"
        )

        align = self.app.language.get_alignment()
        if align == TextAlignment.LTR:
            btn_reset.grid(row=0, column=0, padx=(0, 2))
            self.app.btn_copy.grid(row=0, column=1, padx=2)
            self.app.btn_save.grid(row=0, column=2, padx=(2, 0))
        else:
            self.app.btn_copy.grid(row=0, column=0, padx=(0, 2))
            self.app.btn_save.grid(row=0, column=1, padx=2)
            btn_reset.grid(row=0, column=2, padx=(2, 0))
