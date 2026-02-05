import os, sys
import tkinter as tk
from openpyxl import Workbook
from tkinter import filedialog

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def only_numbers(char):
    return char.isdigit() or char == ""

def export_to_excel(table):
    rows = table.get_children()
    if not rows:
        tk.messagebox.showerror("Error", "No data to export")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx")],
        title="Save Excel File"
    )
    if not file_path:
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Students"
    ws.append(["ID", "Name", "Age", "Address"])
    for row in rows:
        ws.append(table.item(row)["values"])
    wb.save(file_path)
    tk.messagebox.showinfo("Success", "Excel exported successfully!")
    try:
        os.startfile(file_path)
    except:
        pass

def sort_column(table, col, reverse):
    data = [(table.set(k, col), k) for k in table.get_children("")]
    try:
        data.sort(key=lambda t: int(t[0]), reverse=reverse)
    except:
        data.sort(reverse=reverse)
    for index, (val, k) in enumerate(data):
        table.move(k, "", index)
    table.heading(col, command=lambda: sort_column(table, col, not reverse))
