from fastapi import APIRouter, HTTPException
from app.models import Doctor
from app.database import get_db
import psycopg2

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.post("")
async def add_doctor(doctor: Doctor):
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO doctors(name, specialty) VALUES (%s, %s) RETURNING doctor_id",
                    (doctor.name, doctor.specialty)
                )
                new_id = cur.fetchone()[0]
                return {"message": "Doctor added successfully", "doctor_id": new_id}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.get("")
async def get_doctors():
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM doctors"
                )
                rows = cur.fetchall()
                return [{"doctor_id": row[0], "name": row[1], "specialty": row[2]} for row in rows]
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.get("/{doctor_id}")
async def get_doctor(doctor_id: int):
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM doctors WHERE doctor_id = %s",(doctor_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail=f"Doctor with id {doctor_id} not found")
                return {"doctor_id": row[0], "name": row[1], "specialty": row[2]}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.put("/{doctor_id}")
async def update_doctor(doctor_id: int, doctor: Doctor):
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    UPDATE doctors
                    SET name = %s, specialty = %s
                    WHERE doctor_id = %s
                    RETURNING doctor_id, name, specialty
                    ''', (doctor.name, doctor.specialty, doctor_id)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail=f"Doctor with id {doctor_id} not found")
                return {"doctor_id": doctor_id, "name": row[1], "specialty": row[2]}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.delete("/{doctor_id}")
async def delete_doctor(doctor_id: int):
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT doctor_id FROM doctors WHERE doctor_id = %s", (doctor_id,)
                )              
                doctor_id = cur.fetchone()
                if not doctor_id:
                    raise HTTPException(status_code=404, detail=f"Doctor with id {doctor_id} not found")
                cur.execute(
                    "SELECT 1 FROM appointments WHERE doctor_id = %s", (doctor_id,)
                )
                has_appointment = cur.fetchone()
                if has_appointment:
                    raise HTTPException(status_code=404, detail="Cannot delete doctor with appointment")
                cur.execute(
                    "DELETE FROM doctors WHERE doctor_id = %s", (doctor_id,)
                )
                return {"message": f"Doctor with id {doctor_id} has been deleted successfully"} 
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")         