import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# ---------------- DATABASE ----------------

def create_database():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            address TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_student():
    name = name_entry.get()
    age = age_entry.get()
    address = address_entry.get()

    if name == "" or age == "" or address == "":
        messagebox.showerror("Error", "All fields required")
        return

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, age, address) VALUES (?, ?, ?)",
        (name, age, address)
    )
    conn.commit()
    conn.close()

    clear_fields()
    load_students()

def delete_student():
    selected = table.focus()

    if not selected:
        messagebox.showerror("Error", "Select a student")
        return

    student_id = table.item(selected)["values"][0]

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()

    load_students()

def load_students():
    for row in table.get_children():
        table.delete(row)

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        table.insert("", tk.END, values=row)

def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

# ---------------- UI ----------------

root = tk.Tk()
root.title("Student Management System")
root.geometry("600x500")

create_database()

tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root, width=40)
name_entry.pack()

tk.Label(root, text="Age").pack()
age_entry = tk.Entry(root, width=40)
age_entry.pack()

tk.Label(root, text="Address").pack()
address_entry = tk.Entry(root, width=40)
address_entry.pack()

tk.Button(root, text="Save Student", command=save_student).pack(pady=5)
tk.Button(root, text="Delete Selected", command=delete_student).pack(pady=5)

columns = ("ID", "Name", "Age", "Address")
table = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=130)

table.pack(fill="both", expand=True)

load_students()

root.mainloop()
