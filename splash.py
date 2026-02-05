import tkinter as tk
from tkinter import ttk
from utils import resource_path
from dotenv import load_dotenv
import os

load_dotenv("config.env")

APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")

def show_splash(root):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.geometry("420x320+500+300")
    splash.configure(bg="white")

    splash.attributes("-alpha", 0.0)

    def fade(alpha=0):
        alpha += 0.05
        splash.attributes("-alpha", alpha)
        if alpha < 1:
            splash.after(30, lambda: fade(alpha))

    fade()

    # ---------- LOGO (AUTO SCALE) ----------
    original_logo = tk.PhotoImage(file=resource_path("logo.png"))

    max_size = 180   # max width/height allowed
    scale_w = max(1, original_logo.width() // max_size)
    scale_h = max(1, original_logo.height() // max_size)
    scale = max(scale_w, scale_h)

    logo = original_logo.subsample(scale, scale)

    logo_label = tk.Label(splash, image=logo, bg="white")
    logo_label.image = logo
    logo_label.pack(pady=15)
    # ---------------------------------------

    title = tk.Label(
        splash,
        text=APP_NAME,
        font=("Segoe UI", 16, "bold"),
        bg="white"
    )
    title.pack()

    version = tk.Label(
        splash,
        text=f"Version {APP_VERSION}",
        bg="white"
    )
    version.pack(pady=5)

    bar = ttk.Progressbar(
        splash,
        orient="horizontal",
        length=250,
        mode="determinate"
    )
    bar.pack(pady=25)

    def load():
        for i in range(101):
            bar["value"] = i
            splash.update()
            splash.after(15)
        splash.destroy()
        root.deiconify()

    root.withdraw()
    load()