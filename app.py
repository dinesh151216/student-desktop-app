import sqlite3
import tkinter as tk
from tkinter import messagebox

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

    messagebox.showinfo("Saved", "Student saved")

# ---------------- UI ----------------

root = tk.Tk()
root.title("Student Management System")
root.geometry("400x350")

create_database()

tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Age").pack()
age_entry = tk.Entry(root)
age_entry.pack()

tk.Label(root, text="Address").pack()
address_entry = tk.Entry(root)
address_entry.pack()

tk.Button(root, text="Save Student", command=save_student).pack(pady=10)

root.mainloop()
