import os
from contextlib import contextmanager
import psycopg2
from dotenv import load_dotenv

load_dotenv()

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "public"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        yield conn
    finally:
        if conn:
            conn.close() 