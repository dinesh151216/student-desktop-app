import psycopg2, os
from dotenv import load_dotenv

load_dotenv("config.env")

def get_connection():
    return psycopg2.connect(
        host = os.getenv("DB_HOST"),
        database= os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        port = int(os.getenv("DB_PORT", 5432)),
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
