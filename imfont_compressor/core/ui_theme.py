import os
import json
from enum import Enum
import tkinter as tk
from tkinter import ttk
from imfont_compressor.core.utils import get_resource_path

class ColorKeys(Enum):
    # === Backgrounds ===
    BG_ROOT = "backgrounds.bg_root"                         # Root window background
    BG_MAIN_FRAME = "backgrounds.bg_main_frame"             # Main frame background
    BG_CHILD_FRAME = "backgrounds.bg_child_frame"           # Child frame background
    SEPARATOR = "backgrounds.separator"                     # Divider/separator color

    # === Text ===
    LABEL = "text.label"                                    # Default label text color

    # === Input Fields ===
    INPUT_BG = "inputs.inputbox_bg"                         # Input field background
    INPUT_FG = "inputs.inputbox_fg"                         # Input field text color
    INPUT_INSIDE = "inputs.inputbox_inside"                 # Inner background (inset/padding area)
    INPUT_BORDER = "inputs.inputbox_border"                 # Border color (default)
    INPUT_BORDER_FOCUS = "inputs.inputbox_border_focus"     # Border color when focused
    INPUT_LIGHT_FOCUS = "inputs.inputbox_light_focus"       # Glow effect when focused
    INPUT_INSERT_CURSOR = "inputs.inputbox_insert_cursor"   # Cursor (caret) color

    # === Buttons ===
    BUTTON_BG = "buttons.button_bg"                         # Button background (default)
    BUTTON_FG = "buttons.button_fg"                         # Button text (default)
    BUTTON_HOVER_BG = "buttons.button_hover_bg"             # Background on hover
    BUTTON_HOVER_FG = "buttons.button_hover_fg"             # Text on hover
    BUTTON_PRESSED_BG = "buttons.button_pressed_bg"         # Background when pressed
    BUTTON_PRESSED_FG = "buttons.button_pressed_fg"         # Text when pressed
    BUTTON_DISABLED_BG = "buttons.button_disabled_bg"       # Background when disabled
    BUTTON_DISABLED_FG = "buttons.button_disabled_fg"       # Text when disabled
    BUTTON_BORDER = "buttons.button_border"                 # Button border color

    # === Checkboxes ===
    CHECK_BG = "checkbox.button_bg"                         # Background of checkbox
    CHECK_FG = "checkbox.button_fg"                         # Text color of checkbox
    CHECK_ACTIVE_BG = "checkbox.button_active_bg"           # Background when hovered/active
    CHECK_ACTIVE_FG = "checkbox.button_active_fg"           # Text when hovered/active
    CHECK_SELECTED = "checkbox.button_select_color"         # Checkmark or selection color

    # === Comboboxes ===
    COMBO_BG = "combobox.combobox_bg"                       # Dropdown list background
    COMBO_FG = "combobox.combobox_fg"                       # Dropdown text color
    COMBO_SELECT_BG = "combobox.combobox_select_bg"         # Selected option background
    COMBO_SELECT_FG = "combobox.combobox_select_fg"         # Selected option text
    COMBO_FIELD_BG = "combobox.combobox_field"              # Entry field background
    COMBO_ARROW = "combobox.combobox_arrow"                 # Dropdown arrow icon color
    COMBO_FOCUS_HIGHLIGHT = "combobox.combobox_focus_highlight"  # Focus border color
    COMBO_DISABLED_BG = "combobox.combobox_disabled_bg"     # Background when disabled
    COMBO_DISABLED_FG = "combobox.combobox_disabled_fg"     # Text when disabled
    COMBO_HOVER_BG = "combobox.combobox_hover_bg"           # Background on hover
    COMBO_HOVER_FG = "combobox.combobox_hover_fg"           # Text on hover
    COMBO_BORDER = "combobox.combobox_border"               # Combobox border color

    # === Notebook (Tabs) ===
    NOTEBOOK_BG = "notebook.notebook_bg"                    # Notebook container background
    TAB_BG = "notebook.notebook_tab_bg"                     # Tab background (default)
    TAB_FG = "notebook.notebook_tab_fg"                     # Tab text (default)
    TAB_HOVER_BG = "notebook.notebook_tab_hover_bg"         # Background on hover
    TAB_HOVER_FG = "notebook.notebook_tab_hover_fg"         # Text on hover
    TAB_SELECTED_BG = "notebook.notebook_tab_selected_bg"   # Background of selected tab
    TAB_SELECTED_FG = "notebook.notebook_tab_selected_fg"   # Text of selected tab
    TAB_DISABLED_BG = "notebook.notebook_tab_disabled_bg"   # Background when disabled
    TAB_DISABLED_FG = "notebook.notebook_tab_disabled_fg"   # Text when disabled
    TAB_BORDER = "notebook.notebook_tab_border"             # Tab border color (default)
    TAB_SELECTED_BORDER = "notebook.notebook_tab_selected_border"  # Border of selected tab
    TAB_HOVER_BORDER = "notebook.notebook_tab_hover_border"        # Border on hover

    # === Status Colors ===
    STATUS_IDLE = "status.status_idle"                      # Neutral/idle status
    STATUS_SUCCESS = "status.status_success"                # Success/confirmation
    STATUS_WARNING = "status.status_warning"                # Warning/attention
    STATUS_ERROR = "status.status_error"                    # Error/failure indication

class UITheme:
    def __init__(self, app, default_theme="dark", theme_dir=None):
        """
        Initialize the theme handler.
        
        :param default_theme: default theme ID (filename without extension)
        :param theme_dir: directory where theme JSON files are stored
        """
        self.app = app
        self.theme_dir = theme_dir or get_resource_path("assets", "themes")
        self.theme_name = None
        self.theme_raw = {}
        self.color_map = {}
        self.apply_theme(default_theme)

    def apply_theme(self, theme_name):
        """
        Change the current theme by loading a new theme file.
        
        :param theme_name: theme ID to load
        """
        self.load_theme(theme_name)
        self.refresh_colors()

    def load_theme(self, theme_id: str, version: str = None):
        """
        Load and flatten theme colors from JSON file matching theme_id and optional version.

        :param theme_id: theme ID (mandatory, must match 'id' in JSON)
        :param version: optional theme version string to select specific version, defaults to latest if None
        :raises FileNotFoundError: If no theme with the given ID (and version) is found
        :raises ValueError: If the version specified does not exist for the given theme_id
        :raises json.JSONDecodeError: If theme JSON file is malformed
        """
        # Get all available themes (dict: id -> list of theme dicts)
        all_themes = self.list_available_themes()

        if theme_id not in all_themes:
            raise FileNotFoundError(f"[UITheme] Theme ID '{theme_id}' not found.")

        theme_versions = all_themes[theme_id]

        selected_theme = None
        if version is None:
            selected_theme = sorted(theme_versions, key=lambda t: t.get("version", "0"), reverse=True)[0]
        else:
            for t in theme_versions:
                if t.get("version") == version:
                    selected_theme = t
                    break
            if selected_theme is None:
                raise ValueError(f"[UITheme] Theme '{theme_id}' with version '{version}' not found.")

        # Load theme data and flatten colors
        try:
            self.theme_raw = selected_theme
            self.theme_name = f"{theme_id}@{selected_theme.get('version', '1.0')}"
            self.color_map = self._flatten_color_map(selected_theme.get("colors", {}))
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"[UITheme] Failed to parse JSON for theme '{theme_id}@{version}': {e}", e.doc, e.pos)

    def _flatten_color_map(self, color_dict, parent_key=""):
        """
        Recursively flatten nested color dictionaries to a flat dict with dot notation keys.
        
        :param color_dict: nested dict of colors
        :param parent_key: prefix for keys (used during recursion)
        :return: flat dict of colors { "section.color_key": "#hex" }
        """
        items = {}
        for key, value in color_dict.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                items.update(self._flatten_color_map(value, full_key))
            else:
                items[full_key] = value
        return items

    def set_theme_color(self, widget, **theme_options: ColorKeys):
        """
        Apply and store theming information for a widget using keyword args.
        Supports both normal and 'disabled_' prefixed options for disabled state.

        Example:
            set_theme_color(widget,
                bg=ColorKeys.BUTTON_BG,
                fg=ColorKeys.BUTTON_FG,
                disabled_bg=ColorKeys.BUTTON_DISABLED_BG,
                disabled_fg=ColorKeys.BUTTON_DISABLED_FG)

        :param widget: Tkinter widget to apply theming to
        :param theme_options: Widget options (like bg, fg) mapped to ColorKeys enum
        :raises TypeError: If any value is not a ColorKeys enum
        :raises ValueError: If no theme options are provided
        :raises RuntimeError: If applying a color fails
        :raises AttributeError: If widget does not support the given option
        """
        if not theme_options:
            raise ValueError("[Theme] No color options provided.")

        for opt, key in theme_options.items():
            if not isinstance(key, ColorKeys):
                raise TypeError(f"[Theme] Invalid color key for '{opt}': {key} (type={type(key)})")

        # Separate keys
        normal_keys = {}
        disabled_keys = {}

        for k, v in theme_options.items():
            if k.startswith("disabled_"):
                actual_opt = k[len("disabled_"):]
                if not actual_opt:
                    raise ValueError(f"[Theme] Invalid disabled key '{k}': no option specified after prefix.")
                disabled_keys[actual_opt] = v
            else:
                normal_keys[k] = v

        # Store clean keys
        widget._theme_color_keys = {
            "normal": normal_keys,
            "disabled": disabled_keys
        }

        # Determine current widget state
        state = widget.cget("state") if "state" in widget.keys() else "normal"
        use_keys = disabled_keys if state == "disabled" else normal_keys

        # Apply to widget
        for option, color_key in use_keys.items():
            color_value = self.get_color(color_key)
            if option not in widget.keys():
                raise AttributeError(f"[Theme] Widget does not support option '{option}'")
            try:
                widget.configure({option: color_value})
            except Exception as e:
                raise RuntimeError(f"[Theme] Could not set '{option}' with {color_key} on widget: {e}")
    
    def get_color(self, name, fallback=None):
        """
        Retrieve a color hex string by its key.
        `name` can be a string or ColorKeys enum.
        
        :param name: color key (str or ColorKeys)
        :param fallback: fallback color key (str or ColorKeys) if primary not found
        :return: hex color string or magenta "#FF00FF" if not found
        """
        key = name.value if isinstance(name, Enum) else name
        fallback_key = fallback.value if isinstance(fallback, Enum) else fallback
        return self.color_map.get(key) or self.color_map.get(fallback_key) or "#FF00FF"

    def is_valid_color_key(self, key):
        """
        Check if a color key exists in the current theme.
        
        :param key: flattened color key string
        :return: True if exists, False otherwise
        """
        key_str = key.value if isinstance(key, Enum) else key
        return key_str in self.color_map

    def list_available_themes(self, sort: bool = True) -> dict:
        """
        Load available themes from disk, requiring each to explicitly declare an 'id'.

        Rules:
        - Skip any theme JSON without an 'id'.
        - Allow duplicate theme IDs only if versions differ.
        - Return a dict mapping theme_id → list of theme dicts (each dict includes all info).
        - Optionally sort the result by theme 'name' alphabetically.

        :param sort: If True, return the result sorted by theme 'name'.
        :return: dict { theme_id: [theme_data_dict, ...] }
        """
        themes = {}  # Map theme_id -> list of theme dicts (different versions)

        if not os.path.isdir(self.theme_dir):
            print(f"[Theme] Theme directory not found: {self.theme_dir}")
            return themes

        for filename in os.listdir(self.theme_dir):
            if not filename.endswith(".json"):
                continue

            theme_path = os.path.join(self.theme_dir, filename)

            try:
                with open(theme_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if not isinstance(data, dict):
                    print(f"[Theme] Skipping {filename}: Invalid JSON format (not an object)")
                    continue

                theme_id = data.get("id")
                if not theme_id:
                    print(f"[Theme] Skipping {filename}: Missing 'id' field")
                    continue

                colors = data.get("colors")
                if not isinstance(colors, dict):
                    print(f"[Theme] Skipping {filename}: Missing or invalid 'colors'")
                    continue

                data["version"] = str(data.get("version", "1.0"))
                data["name"] = data.get("name", theme_id)

                if theme_id not in themes:
                    themes[theme_id] = [data]
                else:
                    existing_versions = {t["version"] for t in themes[theme_id]}
                    if data["version"] in existing_versions:
                        print(f"[Theme] Skipping duplicate theme '{theme_id}' with version '{data['version']}' (from {filename})")
                    else:
                        themes[theme_id].append(data)

            except Exception as e:
                print(f"[Theme] Failed to load {filename}: {e}")

        if sort:
            themes = dict(sorted(
                themes.items(),
                key=lambda item: item[1][0].get("name", "").lower()
            ))

        return themes
    
    def get_theme_display_list(self):
        """
        Returns a list of display strings for the theme combobox:
        - If a theme has only one version, display only the name.
        - If multiple versions, display name + (vVersion).
        """
        themes = self.list_available_themes()
        display_list = []

        for theme_id, versions in themes.items():
            if len(versions) == 1:
                name = versions[0].get("name", theme_id)
                display_list.append(name)
            else:
                for theme in versions:
                    name = theme.get("name", theme_id)
                    version = theme.get("version", "1.0")
                    display_list.append(f"{name} (v{version})")
        return display_list

    def get_name(self):
        """
        Get the display name of the currently loaded theme.
        Falls back to theme ID if "name" property is missing.
        
        :return: theme display name string
        """
        return self.theme_raw.get("name", self.theme_name)
    
    def refresh_colors(self):
        """Refresh all widget colors based on current theme."""

        if not self.app.initialized:
            return

        def get_color(key: ColorKeys) -> str:
            if not isinstance(key, ColorKeys):
                raise TypeError(f"[Theme] Expected ColorKeys enum, got {type(key)}: {key}")
            return self.get_color(key)

        def widget_supports_option(widget, option: str) -> bool:
            try:
                widget.cget(option)
                return True
            except tk.TclError:
                return False

        def update_widget_colors(widget):
            widget_id = widget.winfo_name() or str(widget)
            theme_keys = getattr(widget, "_theme_color_keys", None)

            if theme_keys:
                state = widget.cget("state") if "state" in widget.keys() else "normal"
                if isinstance(theme_keys, dict) and "normal" in theme_keys and "disabled" in theme_keys:
                    state_keys = theme_keys["disabled"] if state == "disabled" else theme_keys["normal"]
                else:
                    state_keys = theme_keys

                for option, color_key in state_keys.items():
                    if not isinstance(color_key, ColorKeys):
                        raise ValueError(f"[Theme] Widget '{widget_id}' has invalid ColorKeys entry for '{option}': {color_key}")
                    if widget_supports_option(widget, option):
                        try:
                            widget.configure({option: get_color(color_key)})
                        except Exception as e:
                            raise RuntimeError(f"[Theme] Failed to apply '{option}' with {color_key} to '{widget_id}': {e}")
                    else:
                        pass

            else:
                try:
                    if isinstance(widget, tk.Frame):
                        if widget_supports_option(widget, "bg"):
                            widget.configure(bg=get_color(ColorKeys.BG_MAIN_FRAME))

                    elif isinstance(widget, tk.Label):
                        if widget_supports_option(widget, "bg"):
                            widget.configure(bg=get_color(ColorKeys.BG_MAIN_FRAME))
                        if widget_supports_option(widget, "fg"):
                            widget.configure(fg=get_color(ColorKeys.LABEL))

                    elif isinstance(widget, tk.Entry):
                        if widget_supports_option(widget, "bg"):
                            widget.configure(bg=get_color(ColorKeys.INPUT_BG))
                        if widget_supports_option(widget, "fg"):
                            widget.configure(fg=get_color(ColorKeys.INPUT_FG))
                        if widget_supports_option(widget, "insertbackground"):
                            widget.configure(insertbackground=get_color(ColorKeys.INPUT_INSIDE))

                    elif isinstance(widget, tk.Checkbutton):
                        if widget_supports_option(widget, "bg"):
                            widget.configure(bg=get_color(ColorKeys.CHECK_BG))
                        if widget_supports_option(widget, "fg"):
                            widget.configure(fg=get_color(ColorKeys.CHECK_FG))
                        if widget_supports_option(widget, "activebackground"):
                            widget.configure(activebackground=get_color(ColorKeys.CHECK_ACTIVE_BG))
                        if widget_supports_option(widget, "activeforeground"):
                            widget.configure(activeforeground=get_color(ColorKeys.CHECK_ACTIVE_FG))
                        if widget_supports_option(widget, "selectcolor"):
                            widget.configure(selectcolor=get_color(ColorKeys.CHECK_SELECTED))

                    elif isinstance(widget, tk.Button):
                        state = widget.cget("state")
                        if state != "disabled":
                            if widget_supports_option(widget, "bg"):
                                widget.configure(bg=get_color(ColorKeys.BUTTON_BG))
                            if widget_supports_option(widget, "fg"):
                                widget.configure(fg=get_color(ColorKeys.BUTTON_FG))
                        else:
                            if widget_supports_option(widget, "bg"):
                                widget.configure(bg=get_color(ColorKeys.BUTTON_DISABLED_BG))
                            if widget_supports_option(widget, "fg"):
                                widget.configure(fg=get_color(ColorKeys.BUTTON_DISABLED_FG))

                        if widget_supports_option(widget, "activebackground"):
                            widget.configure(activebackground=get_color(ColorKeys.BUTTON_PRESSED_BG))
                        if widget_supports_option(widget, "activeforeground"):
                            widget.configure(activeforeground=get_color(ColorKeys.BUTTON_PRESSED_FG))

                except Exception as fallback_exception:
                    pass

            # Handle TTK widget styles
            if isinstance(widget, ttk.Widget):
                style = ttk.Style()
                try:
                    if isinstance(widget, ttk.Combobox):
                        style.configure('Custom.TCombobox',
                                        fieldbackground=get_color(ColorKeys.COMBO_FIELD_BG),
                                        foreground=get_color(ColorKeys.COMBO_FG),
                                        background=get_color(ColorKeys.COMBO_BG),
                                        arrowcolor=get_color(ColorKeys.COMBO_ARROW))

                        style.map('Custom.TCombobox',
                                fieldbackground=[
                                    ('readonly', get_color(ColorKeys.COMBO_FIELD_BG)),
                                    ('!readonly', get_color(ColorKeys.COMBO_FIELD_BG)),
                                    ('active', get_color(ColorKeys.COMBO_FIELD_BG)),
                                    ('disabled', get_color(ColorKeys.COMBO_DISABLED_BG))
                                ],
                                foreground=[
                                    ('readonly', get_color(ColorKeys.COMBO_FG)),
                                    ('!readonly', get_color(ColorKeys.COMBO_FG)),
                                    ('active', get_color(ColorKeys.COMBO_FG)),
                                    ('disabled', get_color(ColorKeys.COMBO_DISABLED_FG))
                                ],
                                background=[
                                    ('readonly', get_color(ColorKeys.COMBO_BG)),
                                    ('!readonly', get_color(ColorKeys.COMBO_BG)),
                                    ('active', get_color(ColorKeys.COMBO_BG)),
                                    ('disabled', get_color(ColorKeys.COMBO_DISABLED_BG))
                                ],
                                selectbackground=[
                                    ('readonly', get_color(ColorKeys.COMBO_SELECT_BG)),
                                    ('!readonly', get_color(ColorKeys.COMBO_SELECT_BG))
                                ],
                                selectforeground=[
                                    ('readonly', get_color(ColorKeys.COMBO_SELECT_FG)),
                                    ('!readonly', get_color(ColorKeys.COMBO_SELECT_FG))
                                ])

                        widget.configure(style='Custom.TCombobox')

                    elif isinstance(widget, ttk.Notebook):
                        style.theme_use("default")
                        style.configure("Custom.TNotebook",
                                        background=get_color(ColorKeys.NOTEBOOK_BG),
                                        borderwidth=0)

                        style.configure("Custom.TNotebook.Tab",
                                        background=get_color(ColorKeys.TAB_BG),
                                        foreground=get_color(ColorKeys.TAB_FG),
                                        padding=[8, 4],
                                        borderwidth=2)

                        style.map("Custom.TNotebook.Tab",
                            background=[
                                ("selected", get_color(ColorKeys.TAB_SELECTED_BG)),
                                ("active", get_color(ColorKeys.TAB_HOVER_BG)),
                                ("!selected", get_color(ColorKeys.TAB_BG)),
                            ],
                            foreground=[
                                ("selected", get_color(ColorKeys.TAB_SELECTED_FG)),
                                ("active", get_color(ColorKeys.TAB_FG)),
                                ("!selected", get_color(ColorKeys.TAB_FG)),
                            ],
                            bordercolor=[
                                ("selected", get_color(ColorKeys.TAB_SELECTED_BORDER)),
                                ("active", get_color(ColorKeys.TAB_HOVER_BORDER)),
                                ("!selected", get_color(ColorKeys.TAB_BORDER))
                            ])

                        widget.configure(style="Custom.TNotebook")

                    elif isinstance(widget, ttk.Entry):
                        style.configure("Custom.TEntry",
                                        fieldbackground=get_color(ColorKeys.INPUT_BG),
                                        foreground=get_color(ColorKeys.INPUT_FG),
                                        bordercolor=get_color(ColorKeys.INPUT_BORDER),
                                        lightcolor=get_color(ColorKeys.INPUT_INSIDE))

                        style.map("Custom.TEntry",
                                fieldbackground=[
                                    ("disabled", get_color(ColorKeys.BUTTON_DISABLED_BG)),
                                    ("focus", get_color(ColorKeys.INPUT_LIGHT_FOCUS)),
                                    ("!disabled", get_color(ColorKeys.INPUT_BG))
                                ],
                                foreground=[
                                    ("disabled", get_color(ColorKeys.BUTTON_DISABLED_FG)),
                                    ("focus", get_color(ColorKeys.INPUT_FG)),
                                    ("!disabled", get_color(ColorKeys.INPUT_FG))
                                ],
                                bordercolor=[
                                    ("focus", get_color(ColorKeys.INPUT_BORDER_FOCUS)),
                                    ("!focus", get_color(ColorKeys.INPUT_BORDER))
                                ],
                                lightcolor=[
                                    ("focus", get_color(ColorKeys.INPUT_INSIDE)),
                                    ("!focus", get_color(ColorKeys.INPUT_INSIDE))
                                ])

                        widget.configure(style="Custom.TEntry")

                except Exception as ttk_exception:
                    pass

            # Recurse through children
            for child in widget.winfo_children():
                update_widget_colors(child)

        # Start from root widget
        update_widget_colors(self.app.root)
