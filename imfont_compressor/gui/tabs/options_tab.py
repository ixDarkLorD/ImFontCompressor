import tkinter as tk
from tkinter import ttk, font as tkfont
import imfont_compressor.core.events as events
from imfont_compressor.core.app import ImFontCompressorApp
from imfont_compressor.gui.components.buttons import styled_button
from imfont_compressor.core.utils import get_resource_path
from imfont_compressor.core.ui_theme import ColorKeys
from imfont_compressor.core.language import TextAlignment
from imfont_compressor import CURRENT_VERSION, AUTHOR
from PIL import Image, ImageTk

class OptionsTab:
    def __init__(self, app: ImFontCompressorApp, notebook):
        self.app = app
        self.notebook = notebook
        self._create_tab()
        self._setup_language_and_theme_section()
        self._setup_about_content()

    def _create_tab(self):
        self.frame = tk.Frame(self.notebook)
        self.notebook.add(self.frame, text=self.app.language.get("tab.options"))

        try:
            original = Image.open(get_resource_path("assets/logo.png"))

            resized = original.resize((100, 100), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized)

            outline_frame = tk.Frame(
                self.frame,
                highlightbackground="black",
                highlightthickness=2,
                bd=0,
                relief="flat",
                width=104,
                height=104
            )
            outline_frame.place(relx=0.5, rely=0.49, anchor="center")
            self.app.ui_theme.set_theme_color(outline_frame, highlightbackground=ColorKeys.BG_CHILD_FRAME)

            bg_label = tk.Label(outline_frame, image=self.bg_photo, borderwidth=0)
            bg_label.place(relx=0.5, rely=0.5, anchor="center")

            outline_frame.lower()
        except Exception as e:
            print("Error loading background image:", e)

    def _setup_language_and_theme_section(self):
        align = self.app.language.get_alignment()
        is_ltr = align == TextAlignment.LTR
        visuals_font = tkfont.Font(size=12, weight="bold")

        # === Row Container Frame ===
        row_frame = tk.Frame(self.frame, bd=2, relief="ridge")
        row_frame.pack(padx=self.app.pad_x, pady=self.app.pad_y + 4, anchor="center")
        self.app.ui_theme.set_theme_color(row_frame, bg=ColorKeys.BG_CHILD_FRAME)

        # === Language Section ===
        lang_frame = tk.Frame(row_frame, bd=2, relief="sunken")
        lang_frame.pack(
            side="left" if is_ltr else "right",
            padx=(self.app.pad_x, self.app.pad_x // 2),
            pady=self.app.pad_y
        )

        lang_label = tk.Label(
            lang_frame,
            text=self.app.language.get('options.label.language'),
            font=visuals_font
        )
        lang_label.pack(
            side="left" if is_ltr else "right",
            padx=(0, 4) if is_ltr else (4, 0),
            pady=2
        )

        language_names = [name for code, name in self.app.language.get_available_languages()]
        current_lang_name = self.app.language.get_language_name()
        
        self.app.language_combo = ttk.Combobox(
            lang_frame,
            values=language_names,
            state="readonly",
            justify="left" if is_ltr else "right"
        )
        self.app.language_combo.set(current_lang_name if current_lang_name in language_names else language_names[0])
        self.app.language_combo.bind("<<ComboboxSelected>>", lambda e: events.on_language_changed(self.app))
        self.app.language_combo.pack(
            side="left" if is_ltr else "right",
            pady=2
        )

        # === Theme Section ===
        theme_frame = tk.Frame(row_frame, bd=2, relief="sunken")
        theme_frame.pack(
            side="left" if is_ltr else "right",
            padx=(self.app.pad_x // 2, self.app.pad_x),
            pady=self.app.pad_y
        )

        theme_label = tk.Label(
            theme_frame,
            text=self.app.language.get('options.label.theme'),
            font=visuals_font
        )
        theme_label.pack(
            side="left" if is_ltr else "right",
            padx=(0, 4) if is_ltr else (4, 0),
            pady=2
        )

        theme_names = self.app.ui_theme.get_theme_display_list()
        self.app.theme_combo = ttk.Combobox(
            theme_frame,
            values=theme_names,
            state="readonly",
            justify="left" if is_ltr else "right"
        )
        self.app.theme_combo.set(self.app.ui_theme.get_name())
        self.app.theme_combo.bind("<<ComboboxSelected>>", lambda e: events.on_theme_changed(self.app))
        self.app.theme_combo.pack(
            side="left" if is_ltr else "right",
            pady=2
        )

    def _setup_about_content(self):
        container = tk.Frame(self.frame)
        container.place(relx=0.5, rely=1.0, anchor="s", y=-20)

        # Version Label
        version = tk.Label(
            container,
            text=self.app.language.get("options.label.build").format(CURRENT_VERSION),
            justify="center"
        )
        version.grid(row=0, column=1, sticky="ew")

        # Credits Label
        credits = tk.Label(
            container,
            text=self.app.language.get("options.label.credits").format(AUTHOR),
            justify="center"
        )
        credits.grid(row=1, column=1, sticky="ew", pady=(0, self.app.pad_y))

        # Copyright Label
        copyright = tk.Label(
            container,
            text="© 2025",
            justify="center"
        )
        copyright.grid(row=2, column=1, sticky="ew", pady=(0, self.app.pad_y))

        # Layout config
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.columnconfigure(2, weight=1)

        # Discord Button
        discord_btn = styled_button(
            self.app, container, self.app.language.get("options.button.discord"),
            lambda: events.open_discord(self.app),
            width=16
        )
        discord_btn.grid(row=2, column=0, sticky="ew", padx=(0, self.app.pad_x))

        # Update Button
        update_btn = styled_button(
            self.app, container, self.app.language.get("options.button.check_for_updates"),
            lambda: events.check_and_notify_update(self.app),
            width=16
        )
        update_btn.grid(row=2, column=1, sticky="ew")

        # GitHub Button
        github_btn = styled_button(
            self.app, container, self.app.language.get("options.button.github"),
            lambda: events.open_github(self.app),
            width=16
        )
        github_btn.grid(row=2, column=2, sticky="ew", padx=(self.app.pad_x, 0))

        