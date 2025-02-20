import psycopg2
from tabulate import tabulate
from contextlib import contextmanager
import os
import json
from dotenv import load_dotenv
import hashlib
import logging

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

def init_database(db_name: str):
   try:
      conn = psycopg2.connect(
          dbname="postgres",
          user=os.getenv("DB_USER"),
          password=os.getenv("DB_PASSWORD"),
          host=os.getenv("DB_HOST"),
          port=os.getenv("DB_PORT")
      )
      conn.autocommit = True
      cur = conn.cursor()

      # Check if database already exists
      cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
      if cur.fetchone():
         print(f"Database {db_name} already exists")
         return

      # Create database
      cur.execute(f"CREATE DATABASE {db_name}")
      print(f"Database {db_name} created successfully")
      conn.close()
   except psycopg2.Error as e:
      print(f"Database creation error: {e}")
      raise

def show_documents_tables():
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            
            # Show documents table
            print("\n=== Documents Table ===")
            cur.execute("""
                SELECT id, uuid, filename, LEFT(filehash, 8) as hash_preview, 
                       created_at 
                FROM documents 
                ORDER BY id
            """)
            columns = [desc[0] for desc in cur.description]
            results = cur.fetchall()
            print(tabulate(results, headers=columns, tablefmt='psql'))
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        raise

def show_processed_documents_tables():
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            
            # Show processed_documents table
            print("\n=== Processed Documents Table ===")
            cur.execute("""
                SELECT id, doc_uuid, filename, LEFT(filehash, 8) as hash_preview,
                       LEFT(data_structure::text, 30) || '...' as data_preview,
                       created_at
                FROM processed_documents 
                ORDER BY id
            """)
            columns = [desc[0] for desc in cur.description]
            results = cur.fetchall()
            print(tabulate(results, headers=columns, tablefmt='psql'))

    except psycopg2.Error as e:
        print(f"Error displaying tables: {e}")
        raise
   
def init_tables():
    """Initialize database tables if they don't exist"""
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()

            # Create UUID extension if it doesn't exist
            logging.info("Creating UUID extension")
            cur.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")

            # Create documents table with composite key
            logging.info("Creating documents table")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id BIGSERIAL PRIMARY KEY,
                    uuid UUID DEFAULT uuid_generate_v4(),
                    filename TEXT NOT NULL,
                    filehash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT documents_unique_composite UNIQUE (uuid, filename, filehash)
                )
            """)

            # Create processed_documents table with UUID foreign key
            logging.info("Creating processed_documents table")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS processed_documents (
                    id BIGSERIAL PRIMARY KEY,
                    doc_uuid UUID NOT NULL,
                    filename TEXT NOT NULL,
                    filehash TEXT NOT NULL,
                    data_structure JSONB NOT NULL,
                    protocol JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (doc_uuid, filename, filehash) REFERENCES documents(uuid, filename, filehash)
                )
            """)
            conn.commit()
            print("Database tables initialized successfully")

    except psycopg2.Error as e:
        print(f"Database initialization error: {e}")
        raise
    
def drop_tables():
    """Drop all tables if they exist"""
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            
            # Drop tables in correct order (processed_documents depends on documents)
            cur.execute("""
                DROP TABLE IF EXISTS processed_documents;
                DROP TABLE IF EXISTS documents;
            """)
            conn.commit()
            print("Tables dropped successfully")
            
    except psycopg2.Error as e:
        print(f"Error dropping tables: {e}")
        raise

def migrate_existing_documents() -> None:
    """Migrate existing documents to the database"""
    if os.listdir("data"):
      try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            logging.info("Migrating existing documents to the database")
            print(os.listdir("data"))
            print("PROGRESS:")
            for index, filename in enumerate(os.listdir("data")):
                    with open(f"data/{filename}", "rb") as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()
                        cur.execute("INSERT INTO documents (filename, filehash) VALUES (%s, %s)", (filename, file_hash))
                        conn.commit()
                        print(f"\t{index+1}/{len(os.listdir('data'))} documents migrated")
            show_documents_tables()

      except psycopg2.Error as e:
        print(f"Database migration error: {e}")
        raise

def migrate_existing_data_structures() -> None:
    """Migrate existing data structures to the database"""
    if os.listdir("format"):
      try:
          with get_db_connection() as conn:
              cur = conn.cursor()
              logging.info("Migrating existing data structures to the database")
              print(os.listdir("format"))
              print("PROGRESS:")
              for index, file in enumerate(os.listdir("format")):
                filename = file.split(".")[0]
                docname = None
                uuid, filehash = None, None
                for doc in os.listdir("data"):
                  if doc.split(".")[0] == filename:
                    docname = doc
                    cur.execute("SELECT uuid, filehash FROM documents WHERE filename = %s", (doc,)) # need single element tuple
                    result = cur.fetchone()
                    if not result:
                        continue
                    uuid, filehash = result[0], result[1]
                    break

                if uuid and filehash:
                  with open(f"format/{file}", "r") as f:
                    data_structure = json.load(f)
                    data_structure_json: json = json.dumps(data_structure) # Needs to be json binary
                    cur.execute("INSERT INTO processed_documents (doc_uuid, filename, filehash, data_structure) VALUES (%s, %s, %s, %s)", (uuid, docname, filehash, data_structure_json))
                    conn.commit()
                    print(f"\t{index+1}/{len(os.listdir('format'))} documents migrated")
                    show_processed_documents_tables()
      except psycopg2.Error as e:
        print(f"Database migration error: {e}")
        raise

if __name__ == "__main__":
    init_database("public")
    drop_tables()
    init_tables()
    migrate_existing_documents()
    migrate_existing_data_structures()