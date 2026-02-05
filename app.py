import sqlite3
import tkinter as tk

# ---------------- DATABASE SETUP ----------------

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

# ---------------- UI SETUP ----------------

root = tk.Tk()
root.title("Student Management System")
root.geometry("400x300")

create_database()

root.mainloop()
