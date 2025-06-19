import tkinter as tk
from imfont_compressor.core.app import ImFontCompressorApp
from imfont_compressor.core.ui_theme import ColorKeys
from imfont_compressor.core.language import TextAlignment
from imfont_compressor.gui.components.buttons import styled_button
import tkinter.messagebox as messagebox


class UnicodeTab:
    def __init__(self, app: ImFontCompressorApp, container):
        self.app = app
        self.container = container
        self._create_tab()
        self._setup_unicode_tools()

    def _create_tab(self):
        self.frame = tk.Frame(self.container, bd=2, relief="ridge")
        self.container.add(self.frame, text=self.app.language.get("tab.unicode"))

    def _setup_unicode_tools(self):
        align = self.app.language.get_alignment()
        is_ltr = align == TextAlignment.LTR
        justify = "left" if is_ltr else "right"
        anchor = "w" if is_ltr else "e"

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        form_frame = tk.Frame(self.frame, padx=10, pady=10)
        form_frame.grid(row=0, column=0, sticky="nsew")
        self.app.ui_theme.apply_colors(form_frame, bg=ColorKeys.BG_MAIN_FRAME)

        label_font = ("Segoe UI", 10, "bold")

        # Prefix section
        prefix_frame = tk.Frame(form_frame)
        prefix_frame.pack(fill="x", pady=(0, 10))
        self.app.ui_theme.apply_colors(prefix_frame, bg=ColorKeys.BG_CHILD_FRAME)

        prefix_frame.grid_columnconfigure(1 if is_ltr else 0, weight=1)

        label = tk.Label(prefix_frame, text=self.app.language.get("unicode.label.prefix"), font=label_font)
        label.grid(row=0, column=0 if is_ltr else 1, padx=(self.app.pad_x, 0) if is_ltr else (0, self.app.pad_x), pady=self.app.pad_y, sticky=anchor)
        self.app.ui_theme.apply_colors(label, bg=ColorKeys.BG_CHILD_FRAME, fg=ColorKeys.LABEL)

        self.prefix_var = tk.StringVar(value="FONT_")
        entry = tk.Entry(prefix_frame, textvariable=self.prefix_var, width=20, justify=justify)
        entry.grid(row=0, column=1 if is_ltr else 0, sticky=anchor, padx=4)

        # Input section
        input_frame = tk.Frame(form_frame)
        input_frame.pack(fill="x", pady=(0, 10))
        self.app.ui_theme.apply_colors(input_frame, bg=ColorKeys.BG_CHILD_FRAME)

        label = tk.Label(
            input_frame,
            text=self.app.language.get("unicode.label.enter_named_codepoints"),
            font=label_font,
            anchor="center"
        )
        label.pack(anchor="center")
        self.app.ui_theme.apply_colors(label, bg=ColorKeys.BG_CHILD_FRAME, fg=ColorKeys.LABEL)

        self.codepoints_var = tk.StringVar()
        code_entry = tk.Entry(input_frame, textvariable=self.codepoints_var, width=50, justify=justify)
        code_entry.pack(fill="x", padx=self.app.pad_x, pady=(2, self.app.pad_y), anchor=anchor)
        self.codepoints_var.trace_add("write", self.update_defines)
        self.prefix_var.trace_add("write", self.update_defines)

        # Output section
        small_font = ("Courier New", 9)
        self.output = tk.Text(
            form_frame,
            height=4,
            wrap="none",
            font=small_font,
            padx=4,
            pady=2,
            borderwidth=2,
            relief="sunken",
            state="disabled"
        )
        self.output.pack(padx=4, pady=(0, 4), fill="both", expand=True)
        self.output.tag_configure("align", justify=justify)
        self.app.ui_theme.apply_colors(
            self.output,
            bg=ColorKeys.BG_MAIN_FRAME,
            fg=ColorKeys.LABEL,
            disabled_bg=ColorKeys.BG_CHILD_FRAME,
            disabled_fg=ColorKeys.LABEL
        )

        # Copy button
        copy_btn = styled_button(
            self.app,
            form_frame,
            self.app.language.get("unicode.button.copy_output"),
            self.copy_output
        )
        copy_btn.pack(pady=(6, 0))

    def update_defines(self, *_):
        raw_input = self.codepoints_var.get()
        prefix = self.prefix_var.get().strip()

        self.output.configure(state="normal")
        self.output.delete("1.0", tk.END)
        if not raw_input:
            self.output.configure(state="disabled")
            return

        name_counter = {}
        parts = raw_input.strip().split()

        for part in parts:
            if '=' not in part:
                continue

            name, hex_code = part.split('=', 1)
            name = name.strip().upper()
            hex_code = hex_code.strip().lower()

            if not name or not all(c in "0123456789abcdef" for c in hex_code):
                self.output.insert(tk.END, f"// Error: Invalid hex codepoint '{hex_code}' for {name}\n")
                continue

            # Handle duplicate names
            full_name = f"{prefix}{name}"
            if full_name in name_counter:
                name_counter[full_name] += 1
                full_name = f"{full_name}_{name_counter[full_name]}"
            else:
                name_counter[full_name] = 0  # First time

            define = self.unicode_to_define(full_name, hex_code)
            if define:
                self.output.insert(tk.END, define + "\n")
            else:
                self.output.insert(tk.END, f"// Error: Failed to convert codepoint '{hex_code}' for {full_name}\n")

        self.output.configure(state="disabled")
    
    def unicode_to_define(self, name, codepoint_hex):
        try:
            codepoint = int(codepoint_hex, 16)
            utf8_bytes = chr(codepoint).encode("utf-8")
            hex_bytes = ''.join(f"\\x{b:02x}" for b in utf8_bytes)
            return f'#define {name} "{hex_bytes}"  // U+{codepoint_hex.upper()}'
        except Exception:
            return ""

    def copy_output(self):
        self.output.configure(state="normal")
        text = self.output.get("1.0", tk.END).strip()
        self.output.configure(state="disabled")

        if text:
            self.frame.clipboard_clear()
            self.frame.clipboard_append(text)
            self.frame.update()
            messagebox.showinfo(
                title=self.app.language.get("unicode.message.copied_title", "Copied"),
                message=self.app.language.get("unicode.message.copied_body", "Output copied to clipboard.")
            )
