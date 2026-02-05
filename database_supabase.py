import psycopg2

def get_connection():
    return psycopg2.connect(
        host="aws-1-ap-northeast-2.pooler.supabase.com",
        database="postgres",
        user="postgres.npkjtocxtnibodpqcuud",
        password="Disha@01021998@1",
        port = 5432,
        sslmode='require'
    )

def create_database():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id SERIAL PRIMARY KEY,
            name TEXT,
            age INTEGER,
            address TEXT
        )
    """)
    conn.commit()
    conn.close()
