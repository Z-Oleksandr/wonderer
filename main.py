import tkinter as tk
from ui.home_page import HomePage
from ui.settings_page import SettingsPage
import json
import os
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

CONFIG_PATH = "config.json"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wonderer")
        self.geometry("1000x600")

        self.config_data = self.load_config()
        self.base_url = self.config_data.get("base_url", "")

        self.nav_frame = tk.Frame(self, width=150, bg="#2e3f4f")
        self.nav_frame.pack(side="left", fill="y")

        self.content_frame = tk.Frame(self, bg="#f0f0f0")
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.pages = {}
        self.init_navigation()
        self.show_page("Home")

    def init_navigation(self):
        tk.Button(self.nav_frame, text="Home", command=lambda: self.show_page("Home"), bg="#4a6fa5", fg="white").pack(fill="x")
        tk.Button(self.nav_frame, text="Settings", command=lambda: self.show_page("Settings"), bg="#4a6fa5", fg="white").pack(fill="x")

    def show_page(self, name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if name == "Home":
            self.pages[name] = HomePage(self.content_frame, self)
        elif name == "Settings":
            self.pages[name] = SettingsPage(self.content_frame, self)
        self.pages[name].pack(fill="both", expand=True)

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        else:
            return {}

    def save_config(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.config_data, f, indent=2)

if __name__ == "__main__":
    app = App()
    app.mainloop()
