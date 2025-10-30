from fastapi import APIRouter, HTTPException
from app.models import AppointmentIn, AppointmentOut, AppointmentUpdateStatus
from app.database import get_db
from app.utils import check_exists
from typing import List
import psycopg2

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("")
async def add_appointment(appointment: AppointmentIn):
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                check_exists("patients", "patient_id", appointment.patient_id)
                check_exists("doctors", "doctor_id", appointment.doctor_id)
                cur.execute(
                    "INSERT INTO appointments(patient_id, doctor_id, appointment_date) VALUES (%s, %s, %s) RETURNING appointment_id",
                    (appointment.patient_id, appointment.doctor_id, appointment.appointment_date)
                )
                new_id = cur.fetchone()[0]
                return {"message": "Appointment added successfully", "appointment_id": new_id}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")     
    
@router.get("", response_model=List[AppointmentOut])
async def get_appointment():
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT a.appointment_id, p.name, d.name, appointment_date, status
                    FROM appointments a
                    JOIN doctors d ON d.doctor_id = a.doctor_id
                    JOIN patients p on p.patient_id = a.patient_id'''
                )
                rows = cur.fetchall()
                return [{
                    "appointment_id": row[0],
                    "patient": row[1],
                    "doctor": row[2],
                    "appointment_date": row[3],
                    "status": row[4]
                } for row in rows]
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.put("/status/{appt_id}", response_model=AppointmentOut)
async def update_appointment(appt_id: int, update: AppointmentUpdateStatus):
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    UPDATE appointments
                    SET status = %s
                    WHERE appointment_id = %s         
                    RETURNING appointment_id, 
                                (SELECT name FROM patients WHERE patient_id = appointments.patient_id),
                                (SELECT name FROM doctors WHERE doctor_id = appointments.doctor_id),
                                appointment_date, status
                    ''', (update.status, appt_id)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail=f"Appointment with id {appt_id} not found")
                return {
                    "appointment_id": row[0],
                    "patient": row[1],
                    "doctor": row[2],
                    "appointment_date": row[3],
                    "status": row[4]
                }
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    

                
