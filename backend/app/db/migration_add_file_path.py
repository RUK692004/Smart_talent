"""
Migration: Add file_path column to resumes table.
Run this once after the code update to add the column if it doesn't exist.
"""
import psycopg


def run_migration():
    conn = psycopg.connect(
        host="localhost",
        dbname="resume_db",
        user="postgres",
        password="smart",
        port="5432"
    )
    cur = conn.cursor()

    try:
        # Check if column exists
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'resumes' AND column_name = 'file_path'
        """)
        exists = cur.fetchone()

        if not exists:
            cur.execute("ALTER TABLE resumes ADD COLUMN file_path VARCHAR(500);")
            conn.commit()
            print("Migration successful: added file_path column to resumes table.")
        else:
            print("Migration skipped: file_path column already exists.")

    except Exception as e:
        conn.rollback()
        print(f"Migration failed: {str(e)}")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    run_migration()