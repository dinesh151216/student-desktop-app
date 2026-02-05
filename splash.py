import tkinter as tk
from tkinter import ttk
from config import APP_NAME, APP_VERSION
from utils import resource_path

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

    original_logo = tk.PhotoImage(
        file=resource_path("logo.png")
    )

    max_size = 180
    scale = max(
        original_logo.width() // max_size,
        original_logo.height() // max_size,
        1
    )

    logo = original_logo.subsample(scale, scale)
    lbl = tk.Label(splash, image=logo, bg="white")
    lbl.image = logo
    lbl.pack(pady=15)

    tk.Label(
        splash, text=APP_NAME,
        font=("Segoe UI", 16, "bold"),
        bg="white"
    ).pack()

    tk.Label(
        splash,
        text=f"Version {APP_VERSION}",
        bg="white"
    ).pack(pady=5)

    bar = ttk.Progressbar(splash, length=250)
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