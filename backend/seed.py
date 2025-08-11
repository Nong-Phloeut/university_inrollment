import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import Error as Psycopg2Error
import psycopg2

# Load environment variables from .env
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SEEDERS_DIR = os.path.join(BASE_DIR, 'seeders')

def run_seeders():
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Create seed_history table to track applied seed files
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS seed_history (
                filename TEXT PRIMARY KEY,
                applied_at TIMESTAMPTZ DEFAULT now()
            )
        """)
        conn.commit()
        print("Seed history table checked/created.")

        if not os.path.exists(SEEDERS_DIR):
            print(f"Error: Seeders directory not found at {SEEDERS_DIR}")
            return

        seed_files = sorted(f for f in os.listdir(SEEDERS_DIR) if f.endswith('.sql'))

        if not seed_files:
            print(f"No .sql seeder files found in the directory: {SEEDERS_DIR}")
            return

        for filename in seed_files:
            cursor.execute("SELECT 1 FROM seed_history WHERE filename = %s", (filename,))
            if cursor.fetchone():
                print(f"Skipping already seeded file: {filename}")
                continue

            sql_file_path = os.path.join(SEEDERS_DIR, filename)
            try:
                with open(sql_file_path, 'r', encoding='utf-8') as f:
                    sql = f.read()

                if not sql.strip():
                    print(f"Warning: {filename} is empty. Skipping.")
                    continue

                print(f"Seeding {filename}...")

                # Split SQL file into individual statements (handles multiple statements)
                statements = sqlparse.split(sql)

                for statement in statements:
                    if statement.strip():
                        cursor.execute(statement)

                cursor.execute("INSERT INTO seed_history (filename) VALUES (%s)", (filename,))
                conn.commit()
                print(f"✅ Successfully seeded {filename}.")

            except Psycopg2Error as e:
                conn.rollback()
                print(f"ERROR seeding {filename}: {e}")
                print(f"SQL that caused the error (first 200 chars):\n{statement[:200]}...")
            except Exception as e:
                conn.rollback()
                print(f"Unexpected error while seeding {filename}: {e}")

        print("🌱 All seeding completed.")

    except Psycopg2Error as e:
        print(f"Database connection or setup error: {e}")
    except Exception as e:
        print(f"Unexpected error during seeding: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("Database connection closed.")


if __name__ == '__main__':
    run_seeders()
