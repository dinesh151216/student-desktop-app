import tkinter as tk
from database_supabase import create_database
from splash import show_splash
from ui import build_ui
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")

root = tk.Tk()
show_splash(root)
root.title(f"{APP_NAME} v{APP_VERSION}")
root.geometry("800x550")

create_database()
build_ui(root)

root.mainloop()