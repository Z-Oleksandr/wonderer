import tkinter as tk
from tkinter import messagebox
import os

class SettingsPage(tk.Frame):
  def __init__(self, parent, app):
    super().__init__(parent)
    self.app = app

    tk.Label(self, text="Set BaseURL:").pack(pady=(20, 5))

    self.base_url_entry = tk.Entry(self, width=50)
    self.base_url_entry.pack()
    self.base_url_entry.insert(0, self.app.base_url or "")

    tk.Button(self, text="Save", command=self.save_base_url).pack(pady=10)

  def save_base_url(self):
    url = self.base_url_entry.get().strip()
    if not url.startswith("http"):
      messagebox.showerror("Error", "Invalid URL")
      return

    self.app.base_url = url
    self.app.config_data['base_url'] = url
    self.app.save_config()

    messagebox.showinfo("Saved", f"BaseURL saved: {url}")
