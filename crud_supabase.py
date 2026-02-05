from database_supabase import get_connection

selected_id = None

def save_student(name, age, address):
    global selected_id
    conn = get_connection()
    cur = conn.cursor()

    if selected_id is None:
        cur.execute(
            "INSERT INTO students(name,age,address) VALUES(%s,%s,%s)",
            (name, age, address)
        )
    else:
        cur.execute(
            "UPDATE students SET name=%s,age=%s,address=%s WHERE id=%s",
            (name, age, address, selected_id)
        )

    conn.commit()
    conn.close()
    selected_id = None

def delete_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM students WHERE id=%s",
        (student_id,)
    )
    conn.commit()
    conn.close()

def get_all_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows

def search_students(keyword):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM students WHERE name ILIKE %s OR address ILIKE %s",
        (f"%{keyword}%", f"%{keyword}%")
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def count_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM students")
    count = cur.fetchone()[0]
    conn.close()
    return count
