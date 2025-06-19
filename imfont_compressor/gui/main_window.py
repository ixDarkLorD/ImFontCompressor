import tkinter as tk
import tkinter.ttk as ttk

from imfont_compressor.core.app import ImFontCompressorApp
from imfont_compressor.core.ui_theme import ColorKeys
from imfont_compressor.gui.tabs.compressor_tab import CompressorTab
from imfont_compressor.gui.tabs.options_tab import OptionsTab
from imfont_compressor.gui.tabs.unicode_tab import UnicodeTab
from imfont_compressor.core.language import TextAlignment

class MainWindow:
    def __init__(self, app: ImFontCompressorApp):
        self.app = app
        self.tab_canvas_items = []
        self.selected_tab_idx = None
        self.tab_animation_params = {'y_offset': 3, 'steps': 5, 'delay': 20}

        self._setup_tab_container()
        self._setup_tabs()
        self._setup_tab_buttons()

    def _setup_tab_container(self):
        self.app.ui_theme.apply_colors(self.app.root, bg=ColorKeys.BG_ROOT)
        self.tab_bar = tk.Canvas(
            self.app.root,
            height=34,
            bg=self.app.ui_theme.get_color(ColorKeys.BG_ROOT),
            highlightthickness=0       
        )
        self.tab_bar.pack(side="top", fill="x")
        self.tab_container = ttk.Notebook(self.app.root)
        self.tab_container.pack(side="top", fill="both", expand=True)

    def _setup_tabs(self):
        self.compressor_tab = CompressorTab(self.app, self.tab_container)
        self.unicode_tab = UnicodeTab(self.app, self.tab_container)
        self.options_tab = OptionsTab(self.app, self.tab_container)

    def _setup_tab_buttons(self):
        # Clear existing tabs
        for tab_item in self.tab_canvas_items:
            for item_id in tab_item:
                self.tab_bar.delete(item_id)
        self.tab_canvas_items = []

        # Layout configuration
        button_pad_x = 10  # Horizontal padding inside button
        button_pad_y = 6   # Vertical padding inside button
        text_offset_y = 2  # Vertical adjustment for text within button
        radius = 10        # Corner radius
        tab_spacing = 4    # Space between tabs
        base_y = 12        # Base vertical position
        margin = 10        # Margin from window edge

        align = self.app.language.get_alignment()
        is_ltr = align == TextAlignment.LTR
        theme = self.app.ui_theme.get_color

        self.tab_bar.update_idletasks()
        container_width = self.tab_bar.master.winfo_width()

        # Measure all tabs
        tab_metrics = []
        for i in range(self.tab_container.index("end")):
            tab_text = self.tab_container.tab(i, option="text")
            text_id = self.tab_bar.create_text(0, 0, text=tab_text, font=("Segoe UI", 10))
            bbox = self.tab_bar.bbox(text_id)
            self.tab_bar.delete(text_id)
            
            if not bbox:
                bbox = (0, 0, len(tab_text) * (10 if not is_ltr else 8), 20)
            
            width = max(60, bbox[2] - bbox[0] + button_pad_x * 2)
            height = max(25, bbox[3] - bbox[1] + button_pad_y * 2)
            tab_metrics.append((width, height, tab_text, i))

        # For RTL
        if not is_ltr:
            tab_metrics = list(reversed(tab_metrics))

        total_width = sum(w for w, _, _, _ in tab_metrics) + (len(tab_metrics)-1)*tab_spacing

        # Calculate starting position based on direction
        if is_ltr:
            x_position = margin
        else:
            x_position = container_width - margin - total_width
            x_position = max(margin, x_position)

        # Create tabs
        for visual_idx, (width, height, tab_text, logical_idx) in enumerate(tab_metrics):
            rect_id = self._rounded_rect(
                self.tab_bar, x_position, base_y, x_position + width, base_y + height, radius,
                fill=theme(ColorKeys.BUTTON_BG),
                outline=theme(ColorKeys.BUTTON_BORDER)
            )
            
            text_x = x_position + button_pad_x if is_ltr else x_position + width - button_pad_x
            anchor = "nw" if is_ltr else "ne"
            label_id = self.tab_bar.create_text(
                text_x, base_y + text_offset_y,
                anchor=anchor,
                text=tab_text,
                font=("Segoe UI", 10),
                fill=theme(ColorKeys.BUTTON_FG)
            )
            
            if logical_idx == self.selected_tab_idx:
                self.tab_bar.move(rect_id, 0, -self.tab_animation_params['y_offset'])
                self.tab_bar.move(label_id, 0, -self.tab_animation_params['y_offset'])
            
            self.tab_canvas_items.append((rect_id, label_id))
            x_position += width + tab_spacing

            for item_id in (rect_id, label_id):
                self.tab_bar.tag_bind(item_id, "<Enter>", 
                    lambda e, v_idx=visual_idx, l_idx=logical_idx: self._hover_tab(v_idx, l_idx))
                self.tab_bar.tag_bind(item_id, "<Leave>", 
                    lambda e, v_idx=visual_idx, l_idx=logical_idx: self._unhover_tab(v_idx, l_idx))
                self.tab_bar.tag_bind(item_id, "<Button-1>", 
                    lambda e, v_idx=visual_idx, l_idx=logical_idx: self._select_tab(v_idx, l_idx))

        if self.tab_canvas_items and (self.selected_tab_idx is None or self.selected_tab_idx >= len(self.tab_canvas_items)):
            self._select_tab(0, 0)  # Select first tab

    def _select_tab(self, visual_idx, logical_idx):
        if self.selected_tab_idx is not None and self.selected_tab_idx != logical_idx:
            if not self.app.language.get_alignment() == TextAlignment.LTR:
                prev_visual_idx = len(self.tab_canvas_items) - 1 - self.selected_tab_idx
            else:
                prev_visual_idx = self.selected_tab_idx
                
            prev_rect, prev_label = self.tab_canvas_items[prev_visual_idx]
            self._animate_tab(prev_rect, prev_label, move_down=True)
        
        if logical_idx != self.selected_tab_idx:
            self.tab_container.select(logical_idx)
            self.selected_tab_idx = logical_idx
        
        rect_id, label_id = self.tab_canvas_items[visual_idx]
        
        if logical_idx != self.selected_tab_idx or not self._is_tab_elevated(rect_id):
            self._animate_tab(rect_id, label_id, move_up=True)
        
        self.tab_bar.itemconfig(rect_id, fill=self.app.ui_theme.get_color(ColorKeys.BUTTON_PRESSED_BG))
        self.tab_bar.itemconfig(label_id, fill=self.app.ui_theme.get_color(ColorKeys.BUTTON_PRESSED_FG))

    def _is_tab_elevated(self, rect_id):
        current_coords = self.tab_bar.coords(rect_id)
        if not current_coords:
            return False
            
        base_y = 12
        params = self.tab_animation_params
        return current_coords[1] < base_y - (params['y_offset'] / 2)

    def _animate_tab(self, rect_id, label_id, move_up=False, move_down=False):
        current_coords = self.tab_bar.coords(rect_id)
        if not current_coords:
            return
            
        params = self.tab_animation_params
        base_y = 12
        target_y = base_y - (params['y_offset'] if move_up else 0)
        current_y = current_coords[1]
        
        if abs(current_y - target_y) > 0.5:
            step = (target_y - current_y) / params['steps']

            def _move_step(count=0):
                if count < params['steps']:
                    self.tab_bar.move(rect_id, 0, step)
                    self.tab_bar.move(label_id, 0, step)
                    self.tab_bar.after(params['delay'], _move_step, count + 1)
            
            _move_step()
    
    def _hover_tab(self, visual_idx, logical_idx):
        if logical_idx == self.selected_tab_idx:
            return
        rect_id, label_id = self.tab_canvas_items[visual_idx]
        self.tab_bar.itemconfig(rect_id, fill=self.app.ui_theme.get_color(ColorKeys.BUTTON_HOVER_BG))
        self.tab_bar.itemconfig(label_id, fill=self.app.ui_theme.get_color(ColorKeys.BUTTON_HOVER_FG))

    def _unhover_tab(self, visual_idx, logical_idx):
        if logical_idx == self.selected_tab_idx:
            return
        rect_id, label_id = self.tab_canvas_items[visual_idx]
        self.tab_bar.itemconfig(rect_id, fill=self.app.ui_theme.get_color(ColorKeys.BUTTON_BG))
        self.tab_bar.itemconfig(label_id, fill=self.app.ui_theme.get_color(ColorKeys.BUTTON_FG))

    def _rounded_rect(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ] if self.app.language.get_alignment() == TextAlignment.LTR else [
            x2 - radius, y1,
            x1 + radius, y1,
            x1, y1,
            x1, y1 + radius,
            x1, y2 - radius,
            x1, y2,
            x1 + radius, y2,
            x2 - radius, y2,
            x2, y2,
            x2, y2 - radius,
            x2, y1 + radius,
            x2, y1,
        ]
        return canvas.create_polygon(points, smooth=True, splinesteps=36, **kwargs)

    def refresh_colors(self):
        theme = self.app.ui_theme.get_color
        for i, (rect_id, label_id) in enumerate(self.tab_canvas_items):
            bg = theme(ColorKeys.BUTTON_PRESSED_BG if i == self.selected_tab_idx else ColorKeys.BUTTON_BG)
            fg = theme(ColorKeys.BUTTON_PRESSED_FG if i == self.selected_tab_idx else ColorKeys.BUTTON_FG)
            self.tab_bar.itemconfig(rect_id, fill=bg, outline=theme(ColorKeys.BUTTON_BORDER))
            self.tab_bar.itemconfig(label_id, fill=fg)
        self.tab_bar.configure(bg=theme(ColorKeys.BG_ROOT))

    def update(self):
        self._setup_tab_buttons()