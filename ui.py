import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from openpyxl import Workbook
from crud import *
from config import APP_NAME, APP_VERSION
from utils import resource_path

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
        root.iconbitmap(resource_path("icon.ico"))
    except:
        pass

    # SEARCH
    search_frame = tk.Frame(root)
    search_frame.pack(fill="x", padx=10)
    tk.Label(search_frame,text="Search").pack(side="left")
    search_entry = tk.Entry(search_frame,width=30)
    search_entry.pack(side="left")
    tk.Button(search_frame,text="Search",
        command=do_search).pack(side="left")

    # FORM
    form = tk.Frame(root)
    form.pack()

    tk.Label(form,text="Name").grid(row=0,column=0)
    name_entry=tk.Entry(form)
    name_entry.grid(row=0,column=1)

    tk.Label(form,text="Age").grid(row=1,column=0)
    age_entry=tk.Entry(form)
    age_entry.grid(row=1,column=1)

    tk.Label(form,text="Address").grid(row=2,column=0)
    address_entry=tk.Entry(form)
    address_entry.grid(row=2,column=1)

    tk.Button(form,text="Save",
        command=save_clicked).grid(row=3,column=0)
    tk.Button(form,text="Delete",
        command=delete_clicked).grid(row=3,column=1)

    # TABLE
    table = ttk.Treeview(
        root,
        columns=("ID","Name","Age","Address"),
        show="headings"
    )

    for c in ("ID","Name","Age","Address"):
        table.heading(c,text=c)
    table.pack(fill="both",expand=True)
    table.bind("<<TreeviewSelect>>",on_select)

    status_label=tk.Label(root)
    status_label.pack(fill="x")

    load_table()

def show_about():
    messagebox.showinfo(
        "About",
        f"{APP_NAME}\nVersion {APP_VERSION}"
    )

def save_clicked():
    save_student(
        name_entry.get(),
        age_entry.get(),
        address_entry.get()
    )
    load_table()

def delete_clicked():
    sel=table.selection()
    if not sel:
        return
    sid=table.item(sel)["values"][0]
    delete_student(sid)
    load_table()

def load_table():
    table.delete(*table.get_children())
    for row in get_all_students():
        table.insert("", "end", values=row)
    status_label.config(
        text=f"Total Students: {count_students()}"
    )

def do_search():
    table.delete(*table.get_children())
    for row in search_students(search_entry.get()):
        table.insert("", "end", values=row)

def on_select(e):
    row=table.item(table.focus())["values"]
    if row:
        name_entry.delete(0,"end")
        name_entry.insert(0,row[1])
        age_entry.delete(0,"end")
        age_entry.insert(0,row[2])
        address_entry.delete(0,"end")
        address_entry.insert(0,row[3])
