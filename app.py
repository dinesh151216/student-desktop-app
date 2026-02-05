import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

selected_id = None

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

# ---------------- CRUD ----------------

def update_status():
    global status_label

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    conn.close()

    status_label.config(text=f"Total Students: {count}")


def save_student():
    global selected_id

    name = name_entry.get()
    age = age_entry.get()
    address = address_entry.get()

    if name == "" or age == "" or address == "":
        messagebox.showerror("Error", "All fields required")
        return

    if not age.isdigit():
        messagebox.showerror("Error", "Age must be a number")
        return

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    if selected_id is None:
        cursor.execute(
            "INSERT INTO students (name, age, address) VALUES (?, ?, ?)",
            (name, age, address)
        )
    else:
        cursor.execute(
            "UPDATE students SET name=?, age=?, address=? WHERE id=?",
            (name, age, address, selected_id)
        )

    conn.commit()
    conn.close()

    clear_fields()
    load_students()
    update_status()
    selected_id = None

def delete_student():
    global table

    selected = table.selection()
    if not selected:
        messagebox.showerror("Error", "Select a student")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if not confirm:
        return

    student_id = table.item(selected)["values"][0]

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()

    load_students()
    clear_fields()
    update_status()

def on_row_select(event):
    global selected_id
    selected = table.focus()
    values = table.item(selected)["values"]

    if values:
        selected_id = values[0]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])
        age_entry.delete(0, tk.END)
        age_entry.insert(0, values[2])
        address_entry.delete(0, tk.END)
        address_entry.insert(0, values[3])

def search_students():
    keyword = search_entry.get()

    for row in table.get_children():
        table.delete(row)

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ? OR address LIKE ?",
        (f"%{keyword}%", f"%{keyword}%")
    )
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        table.insert("", tk.END, values=row)

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
    update_status()

def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

def only_numbers(char):
    return char.isdigit() or char == ""

def sort_column(col, reverse):
    global table

    data = [(table.set(k, col), k) for k in table.get_children("")]

    try:
        data.sort(key=lambda t: int(t[0]), reverse=reverse)
    except:
        data.sort(reverse=reverse)

    for index, (val, k) in enumerate(data):
        table.move(k, "", index)

    table.heading(col, command=lambda: sort_column(col, not reverse))


# ---------------- UI ----------------

root = tk.Tk()
root.title("Student Management System")
root.geometry("800x550")
root.iconbitmap(default="icon.ico")

create_database()

# -------- SEARCH BAR --------

search_frame = tk.Frame(root)
search_frame.pack(fill="x", padx=10, pady=5)

tk.Label(search_frame, text="Search").pack(side="left")
search_entry = tk.Entry(search_frame, width=40)
search_entry.pack(side="left", padx=5)
tk.Button(search_frame, text="Search", command=search_students).pack(side="left")

# -------- FORM + BUTTONS --------

middle_frame = tk.Frame(root)
middle_frame.pack(fill="x", padx=10)

form_frame = tk.Frame(middle_frame)
form_frame.pack(side="left", padx=20)

tk.Label(form_frame, text="Name").grid(row=0, column=0, sticky="w")
name_entry = tk.Entry(form_frame, width=30)
name_entry.grid(row=0, column=1, pady=3)

tk.Label(form_frame, text="Age").grid(row=1, column=0, sticky="w")
# age_entry = tk.Entry(form_frame, width=30)
vcmd = (root.register(only_numbers), '%P')
age_entry = tk.Entry(form_frame, width=30, validate="key", validatecommand=vcmd)

age_entry.grid(row=1, column=1, pady=3)

tk.Label(form_frame, text="Address").grid(row=2, column=0, sticky="w")
address_entry = tk.Entry(form_frame, width=30)
address_entry.grid(row=2, column=1, pady=3)

button_frame = tk.Frame(middle_frame)
button_frame.pack(side="left", padx=30)

tk.Button(button_frame, text="Save / Update", width=15, command=save_student).pack(pady=5)
tk.Button(button_frame, text="Delete", width=15, command=delete_student).pack(pady=5)
tk.Button(button_frame, text="Clear", width=15, command=clear_fields).pack(pady=5)

# -------- TABLE --------

table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("ID", "Name", "Age", "Address")
table = ttk.Treeview(table_frame, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col, command=lambda c=col: sort_column(c, False))
    table.column(col, width=180)

table.bind("<<TreeviewSelect>>", on_row_select)

table.pack(fill="both", expand=True)

status_label = tk.Label(
    root,
    text="Total Students: 0",
    anchor="w",
    relief="sunken",
    padx=10
)
status_label.pack(side="bottom", fill="x")

load_students()

root.mainloop()
