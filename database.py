import sqlite3

DB_PATH = "jobs.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_database():
    conn = get_connection()

    conn.execute(""" 
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT NOT NULL,
            company TEXT NOT NULL,
            title TEXT NOT NULL,
            first_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id, company) 
        )
    """)

    conn.commit()
    conn.close()

def insert_job(id, company, title):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO jobs (id, company, title)
        VALUES (?, ?, ?)
        """,
        (
            id,
            company,
            title
        )
    )

    conn.commit()
    conn.close()

def job_exists(id, company) -> bool:
    conn = get_connection()

    result = conn.execute(
        """
        SELECT COUNT(*) FROM jobs
        WHERE id = ? AND company = ?
        """,
        (
            id,
            company
        )
    ).fetchone()[0]
    conn.close()

    # If count > 0, that job already exists in the db
    return result > 0

def get_all_jobs():
    conn = get_connection()

    res = conn.execute(
        """
        SELECT * FROM jobs
        """
    ).fetchall()
    conn.close()

    return res

def delete_all_jobs():
    conn = get_connection()

    conn.execute(
        """
        DELETE FROM jobs
        """
    )

    conn.commit()
    conn.close()