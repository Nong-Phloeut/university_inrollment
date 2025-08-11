import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import Error as Psycopg2Error

# Load environment variables from .env
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

# --- CHANGE MADE HERE ---
# MIGRATIONS_DIR now points to the 'migrations' subdirectory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MIGRATIONS_DIR = os.path.join(BASE_DIR, 'migrations')
# --- END CHANGE ---

def run_migrations():
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Create migration_history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS migration_history (
                filename TEXT PRIMARY KEY,
                applied_at TIMESTAMPTZ DEFAULT now()
            )
        """)
        conn.commit()
        print("Migration history table checked/created.")

        # Ensure the migrations directory exists
        if not os.path.exists(MIGRATIONS_DIR):
            print(f"Error: Migration directory not found at {MIGRATIONS_DIR}")
            return

        files = sorted(f for f in os.listdir(MIGRATIONS_DIR) if f.endswith('.sql'))

        if not files:
            print(f"No .sql migration files found in the directory: {MIGRATIONS_DIR}")
            return

        for filename in files:
            cursor.execute("SELECT 1 FROM migration_history WHERE filename = %s", (filename,))
            if cursor.fetchone():
                print(f"Skipping {filename}")
                continue

            print(f"Applying {filename}...")
            sql_file_path = os.path.join(MIGRATIONS_DIR, filename)
            try:
                with open(sql_file_path, 'r') as f:
                    sql = f.read()
                    if not sql.strip():
                        print(f"Warning: {filename} is empty or contains only whitespace. Skipping.")
                        continue
                    cursor.execute(sql)
                cursor.execute("INSERT INTO migration_history (filename) VALUES (%s)", (filename,))
                conn.commit()
                print(f"Successfully applied {filename}.")
            except Psycopg2Error as e:
                conn.rollback()
                print(f"ERROR applying {filename}: {e}")
                print(f"SQL that caused the error (first 200 chars):\n{sql[:200]}...")
            except Exception as e:
                conn.rollback()
                print(f"An unexpected error occurred while applying {filename}: {e}")


        print("✅ All migration attempts completed.")

    except Psycopg2Error as e:
        print(f"Database connection or initial setup error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during migration process: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("Database connection closed.")


if __name__ == '__main__':
    run_migrations()