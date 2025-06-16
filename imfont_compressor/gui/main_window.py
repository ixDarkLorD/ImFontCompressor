from tkinter import ttk
from imfont_compressor.gui.tabs.main_tab import MainTab
from imfont_compressor.gui.tabs.options_tab import OptionsTab

class MainWindow:
    def __init__(self, app):
        self.app = app
        self._setup_notebook()
        self._setup_tabs()

    def _setup_notebook(self):
        self.notebook = ttk.Notebook(self.app.root)
        self.notebook.grid(row=0, column=0, sticky="nsew")

    def _setup_tabs(self):
        self.main_tab = MainTab(self.app, self.notebook)
        self.options_tab = OptionsTab(self.app, self.notebook)
