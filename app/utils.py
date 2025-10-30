from fastapi import HTTPException
from app.database import get_db

def check_exists(table: str, column: str, value: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT 1 FROM {table} WHERE {column} = %s", (value,))
            has_id = cur.fetchone()
            if not has_id:
                raise HTTPException(status_code=404, detail=f"{table[:-1].capitalize()} not found")
            return True