import psycopg2
from psycopg2.extensions import connection

DB_CONFIG = {
    "host": "localhost",
    "database": "hospital_db",
    "user": "postgres",
    "password": "1234" 
}

def get_db() -> connection:
    return psycopg2.connect(**DB_CONFIG)