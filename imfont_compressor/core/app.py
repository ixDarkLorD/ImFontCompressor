import tkinter as tk
from tkinter import font as tkfont
from imfont_compressor.core.ui_theme import UITheme, ColorKeys
from imfont_compressor.core.language import Language
from imfont_compressor.core.utils import get_encoding_key, get_resource_path

class ImFontCompressorApp:    
    def __init__(self):
        self.initialized = False
        self.language = Language(self)
        self.ui_theme = UITheme(self)

        self.root = None
        self.last_output_text = None
        self.last_output_file = None

        self._create_root_window()
        self._init_widget_references()
        self._init_theme_settings()
        
        from imfont_compressor.core.config import load_config
        load_config(self, True)

    def _init_widget_references(self):
        self.font_input = None
        self.symbol_name_input = None
        self.encoding_combo = None
        self.theme_combo = None
        self.language_combo = None
        self.btn_copy = None
        self.btn_save = None
        self.btn_compress = None
        self.status_label = None

    def _init_theme_settings(self):
        self.pad_x = 10
        self.pad_y = 8
        self._init_theme_variables()

    def _init_theme_variables(self):
        self.var_encoding = tk.StringVar()
        self.var_encoding.set(get_encoding_key())
        self.var_nocompress = tk.BooleanVar()
        self.var_nostatic = tk.BooleanVar()
        self.var_header = tk.BooleanVar()

    def _create_root_window(self):
        try:
            from tkinterdnd2 import TkinterDnD
            self.root = TkinterDnD.Tk()
        except ImportError:
            self.root = tk.Tk()

        self.root.withdraw()
        self.root.title("ImFont Compressor")
        self.root.iconbitmap(get_resource_path("assets/icon.ico"))
        self.root.resizable(False, False)
        set

    def _create_splash_screen(self):
        self.splash = tk.Toplevel(self.root, bd=8, relief="ridge")
        self.splash.overrideredirect(True)
        self.splash.configure(bg=self.ui_theme.get_color(ColorKeys.BG_MAIN_FRAME))

        width, height = 300, 200
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)
        self.splash.geometry(f"{width}x{height}+{x}+{y}")

        # === Logo image ===
        try:
            from PIL import Image, ImageTk
            image = Image.open(get_resource_path("assets/logo.png"))
            image = image.resize((80, 80))
            self.splash_img = ImageTk.PhotoImage(image)
            image_label = tk.Label(self.splash, image=self.splash_img, bg=self.ui_theme.get_color(ColorKeys.BG_MAIN_FRAME), borderwidth=0)
            image_label.pack(pady=(20, 10))
        except Exception as e:
            print(f"Error loading splash image: {e}")

        # === App Title ===
        title_label = tk.Label(
            self.splash,
            text=self.language.get("ui.title"),
            font=tkfont.Font(size=16, weight="bold"),
            fg=self.ui_theme.get_color(ColorKeys.LABEL),
            bg=self.ui_theme.get_color(ColorKeys.BG_MAIN_FRAME)
        )
        title_label.pack(pady=(0, 6))

        # === Loading Text ===
        self.loading_label = tk.Label(
            self.splash,
            text=self.language.get("ui.loading"),
            font=tkfont.Font(size=11),
            fg=self.ui_theme.get_color(ColorKeys.LABEL),
            bg=self.ui_theme.get_color(ColorKeys.BG_MAIN_FRAME)
        )
        self.loading_label.pack()

        # === Start loading animation ===
        self._loading_dot_count = 0
        self._animate_loading_text()

        self.splash.update()

    def setup_gui(self):
        self._create_splash_screen()

        self.root.after(100, lambda: self._continue_gui_setup())
        self.root.mainloop()

    def _continue_gui_setup(self):
        self._init_theme_settings()

        from imfont_compressor.gui.main_window import MainWindow
        self.main_window = MainWindow(self)

        from imfont_compressor.core.config import load_config
        load_config(self)

        self.root.after(800, self._finalize_gui_setup)

    def _finalize_gui_setup(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.initialized = True
        self.ui_theme.app = self
        self.ui_theme.refresh_colors()

        if hasattr(self, "splash") and self.splash.winfo_exists():
            self.splash.destroy()

        self.root.after(40, self._show_centered_main_window)

    def _show_centered_main_window(self):
        self.root.update_idletasks()
        self.root.update()
        self.root.deiconify()

        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _animate_loading_text(self):
        dots = "." * (self._loading_dot_count % 4)

        from imfont_compressor.core.language import TextAlignment
        align = self.language.get_alignment()
        if align == TextAlignment.LTR:
            text = f"{self.language.get("ui.loading")}{dots}" 
        else:
            text = f"{dots}{self.language.get("ui.loading")}"

        self.loading_label.config(text=text)
        self._loading_dot_count += 1
        self.splash.after(500, self._animate_loading_text)

    def on_close(self):
        from imfont_compressor.core.config import save_config
        save_config(self)
        self.root.destroy()
