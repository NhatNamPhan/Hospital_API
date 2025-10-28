import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "port": os.getenv("DB_PORT", "5432")
}

# Create a connection pool
connection_pool = pool.SimpleConnectionPool(1, 20, **DB_CONFIG)

@contextmanager
def get_db():
    conn = connection_pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        connection_pool.putconn(conn)