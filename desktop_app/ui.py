import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from openpyxl import Workbook

from api_client import *
# from crud_supabase import *
from utils import *
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")

selected_id = None
table = None
name_entry = age_entry = address_entry = search_entry = status_label = None

def build_ui(root):

    global table,name_entry,age_entry,address_entry,search_entry,status_label

    # MENU
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=show_about)

    try:
        root.iconbitmap(resource_path("assets/icon.ico"))
    except:
        pass

    # -------- SEARCH BAR --------

    search_frame = tk.Frame(root)
    search_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(search_frame, text="Search").pack(side="left")
    search_entry = tk.Entry(search_frame, width=40)
    search_entry.pack(side="left", padx=5)
    tk.Button(search_frame, text="Search", command=do_search).pack(side="left")

    # -------- FORM + BUTTONS --------
    # FORM
    middle_frame = tk.Frame(root)
    middle_frame.pack(fill="x", padx=10)
    
    form_frame = tk.Frame(middle_frame)
    form_frame.pack(side="left", padx=20)

    tk.Label(form_frame,text="Name").grid(row=0,column=0, sticky="w")
    name_entry=tk.Entry(form_frame, width=30)
    name_entry.grid(row=0,column=1, pady=3)

    tk.Label(form_frame,text="Age").grid(row=1,column=0, sticky="w")
    # age_entry=tk.Entry(form_frame, width=30)
    vcmd = (root.register(only_numbers), '%P')
    age_entry = tk.Entry(form_frame, width=30, validate="key", validatecommand=vcmd)
    age_entry.grid(row=1,column=1, pady=3)

    tk.Label(form_frame, text="Address").grid(row=2, column=0, sticky="w")
    address_entry = tk.Entry(form_frame, width=30)
    address_entry.grid(row=2, column=1, pady=3)

    # TABLE
    table = ttk.Treeview(
        root,
        columns=("ID","Name","Age","Address"),
        show="headings"
    )

    for col in ("ID","Name","Age","Address"):
        table.heading(col,text=col, command=lambda c=col: sort_column(table, c, False))
        table.column(col, width=180)
    table.pack(fill="both",expand=True, padx=10, pady=10)
    table.bind("<<TreeviewSelect>>",on_select)

    button_frame = tk.Frame(middle_frame)
    button_frame.pack(side="left", padx=30)

    tk.Button(button_frame, text="Save / Update", width=15, command=save_clicked).pack(pady=5)
    tk.Button(button_frame, text="Delete", width=15, command=delete_clicked).pack(pady=5)
    tk.Button(button_frame, text="Clear", width=15, command=clear_fields).pack(pady=5)
    tk.Button(button_frame, text="Export Excel", width=15, command=lambda: export_to_excel(table)).pack(pady=5)

    status_label = tk.Label(
        root,
        text="Total Students: 0",
        anchor="w",
        relief="sunken",
        padx=10
    )
    status_label.pack(side="bottom", fill="x")

    load_table()

def show_about():
    messagebox.showinfo(
            "About",
            f"{APP_NAME}\n"
            f"Version: {APP_VERSION}\n\n"
            "Developed by Dinesh Dhankhar\n"
            "© 2026"
        )

def save_clicked():
    global selected_id
    data = {
        "name": name_entry.get(),
        "age": age_entry.get(),
        "address": address_entry.get()
    }
    if data['name'] == "" or data['age'] == "" or data['address'] == "":
        messagebox.showerror("Error", "All fields required")
        return
    if not data['age'].isdigit():
        messagebox.showerror("Error", "Age must be a number")
        return
    if selected_id is None:
        create_student(data)
    else:
        update_student(selected_id, data)
    clear_fields()
    load_table()
    selected_id = None

def delete_clicked():
    sel=table.selection()
    if not sel:
        messagebox.showerror("Error", "Select a student")
        return
    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )
    if not confirm:
        return
    sid=table.item(sel)["values"][0]
    delete_student(sid)
    clear_fields()
    load_table()

def load_table():
    table.delete(*table.get_children())
    for s in get_students():
        table.insert("", tk.END, values=(s["id"], s["name"], s["age"], s["address"]))
    status_label.config(
        text=f"Total Students: {count_students()}"
    )

def do_search():
    table.delete(*table.get_children())
    for s in search_student(search_entry.get()):
        table.insert("", tk.END, values=(s["id"], s["name"], s["age"], s["address"]))

def on_select(e):
    global selected_id
    row=table.item(table.focus())["values"]
    if row:
        selected_id = row[0]
        
        name_entry.delete(0,"end")
        name_entry.insert(0,row[1])
        
        age_entry.delete(0,"end")
        age_entry.insert(0,row[2])

        address_entry.delete(0,"end")
        address_entry.insert(0,row[3])

def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
