import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "port": os.getenv("DB_PORT", "5432")
}

def get_db() -> connection:
    return psycopg2.connect(**DB_CONFIG)