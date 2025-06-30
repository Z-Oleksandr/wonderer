import tkinter as tk
from tkinter import messagebox
import json
import requests
import datetime

class HomePage(tk.Frame):
  def __init__(self, parent, app):
    super().__init__(parent)
    self.app = app

    # BaseURL and TestConnection
    top_frame = tk.Frame(self)
    top_frame.pack(fill="x", padx=10, pady=10)

    tk.Label(top_frame, text="BaseURL:").pack(side="left")
    self.base_url_label = tk.Label(top_frame, text=self.app.base_url or "[Not Set]", fg="blue")
    self.base_url_label.pack(side="left", padx=5)

    tk.Button(top_frame, text="Test Connection", command=self.test_connection).pack(side="left", padx=10)

    # Request section
    request_frame = tk.Frame(self)
    request_frame.pack(side="left", fill="y", padx=10, pady=10)

    tk.Label(request_frame, text="Route:").pack(anchor="w")
    self.route_entry = tk.Entry(request_frame, width=40)
    self.route_entry.pack()

    self.method_var = tk.StringVar(value="GET")
    tk.Radiobutton(request_frame, text="GET", variable=self.method_var, value="GET").pack(anchor="w")
    tk.Radiobutton(request_frame, text="POST", variable=self.method_var, value="POST").pack(anchor="w")

    tk.Label(request_frame, text="Payload (JSON):").pack(anchor="w")
    self.payload_text = tk.Text(request_frame, height=10, width=50)
    self.payload_text.pack()

    tk.Button(request_frame, text="Send Request", command=self.send_request).pack(pady=10)

    # Output Terminal
    output_frame = tk.Frame(self)
    output_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    tk.Label(output_frame, text="Output:").pack(anchor="w")
    self.output_box = tk.Text(
      output_frame, 
      bg="black", 
      fg="white", 
      wrap="word",
      state="disabled"
    )
    self.output_box.pack(fill="both", expand=True)

  def log(self, text):
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S] ")
    self.output_box.config(state="normal")
    self.output_box.insert("end", timestamp + text + "\n")
    self.output_box.see("end")
    self.output_box.config(state="disabled")

  def test_connection(self):
    if not self.app.base_url:
      messagebox.showwarning("Warning", "BaseURL not set in Settings")
      return
    try:
      res = requests.get(f"{self.app.base_url}/")
      self.log(f"Test Connection Status: {res.status_code},\n Message: {res.text.strip()}")
    except Exception as e:
      self.log(f"Text Connection Failed: {str(e)}")

  def send_request(self):
    if not self.app.base_url:
      messagebox.showwarning("Warning", "BaseURL not set in Settings")
      return

    route = self.route_entry.get().strip()
    url = self.app.base_url.rstrip("/") + "/" + route.lstrip("/")
    method = self.method_var.get()
    payload = self.payload_text.get("1.0", "end").strip()

    headers = {"Content-Type": "application/json"}

    try:
      json_payload = json.loads(payload) if payload else {}
    except json.JSONDecodeError as e:
      self.log(f"Json Error: {e}")
      return

    try:
      if method == "GET":
        res = requests.get(url, params=json_payload, headers=headers)
      else:
        res = requests.post(url, json=json_payload, headers=headers)
      
      self.log(f"{method} {url} => {res.status_code},\n{res.text}")
    except Exception as e:
      self.log(f"Request failed: {str(e)}")
