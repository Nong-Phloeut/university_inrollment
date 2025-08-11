import psycopg2
from config.db_config import DB_CONFIG
from psycopg2.extras import RealDictCursor  # ✅ import

def get_connection():
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        dbname=DB_CONFIG["database"],
        cursor_factory=RealDictCursor 
    )
