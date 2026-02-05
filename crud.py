import sqlite3
from tkinter import messagebox

selected_id = None

def save_student(name, age, address):
    global selected_id
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    if selected_id is None:
        cur.execute(
            "INSERT INTO students(name,age,address) VALUES(?,?,?)",
            (name, age, address)
        )
    else:
        cur.execute(
            "UPDATE students SET name=?,age=?,address=? WHERE id=?",
            (name, age, address, selected_id)
        )

    conn.commit()
    conn.close()
    selected_id = None

def delete_student(student_id):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()

def get_all_students():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()
    return rows

def search_students(keyword):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM students WHERE name LIKE ? OR address LIKE ?",
        (f"%{keyword}%", f"%{keyword}%")
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def count_students():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM students")
    c = cur.fetchone()[0]
    conn.close()
    return c
