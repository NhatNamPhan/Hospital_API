from fastapi import APIRouter, HTTPException
from app.models import Doctor, DoctorStatistics
from app.utils import check_exists
from app.database import get_db
from typing import List
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

@router.get("/stats", response_model=List[DoctorStatistics])
async def get_doctor_statistics():
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT d.name, d.specialty, count(a.appointment_id), SUM(CASE WHEN a.status = 'done' THEN 1 ELSE 0 END)
                    FROM doctors d
                    LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
                    GROUP BY d.doctor_id'''
                )
                rows = cur.fetchall()
                return [
                    {
                        "name": row[0],
                        "specialty": row[1],
                        "total_appointment": row[2],
                        "completed": row[3]
                    } for row in rows
                ]
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}") 

@router.get("/{doctor_id}")
async def get_doctor(doctor_id: int):
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                check_exists("doctors", "doctor_id", doctor_id)
                cur.execute(
                    "SELECT * FROM doctors WHERE doctor_id = %s",(doctor_id,)
                )
                row = cur.fetchone()
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
                check_exists("doctors", "doctor_id", doctor_id)
                cur.execute('''
                    UPDATE doctors
                    SET name = %s, specialty = %s
                    WHERE doctor_id = %s
                    RETURNING doctor_id, name, specialty
                    ''', (doctor.name, doctor.specialty, doctor_id)
                )
                row = cur.fetchone()
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
                check_exists("doctors", "doctor_id", doctor_id)
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
    