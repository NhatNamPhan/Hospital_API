from fastapi import APIRouter, HTTPException
from app.models import Patient, HistoryPatient, ApptOut, PrescriptionOutNotId
from app.utils import check_exists
from app.database import get_db
import psycopg2

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("")
async def add_patient(patient: Patient):
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO patients(name, gender, birth_date, phone) VALUES (%s, %s, %s, %s) RETURNING patient_id",
                    (patient.name, patient.gender, patient.birth_date, patient.phone)
                )
                new_id = cur.fetchone()[0]
                return {"message": "Patient added successfully", "patient_id": new_id}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("")
async def get_patients():
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM patients"
                )
                rows = cur.fetchall()
                return [{"patient_id": row[0], "name": row[1], "gender": row[2], "birth_date": row[3], "phone": row[4]} for row in rows]
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{patient_id}")
async def get_patient(patient_id: int):
    try: 
        with get_db() as conn:
            with conn.cursor() as cur:
                check_exists("patients", "patient_id", patient_id)
                cur.execute(
                    "SELECT * from patients WHERE patient_id = %s", (patient_id,)
                )
                row = cur.fetchone()
                return {"patient_id": patient_id, "name": row[1], "gender": row[2], "birth_date": row[3], "phone": row[4]}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/{patient_id}")
async def update_patient(patient_id: int, patient: Patient):           
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                check_exists("patients", "patient_id", patient_id)
                cur.execute('''
                    UPDATE patients
                    SET name = %s, gender = %s, birth_date = %s, phone = %s
                    WHERE patient_id = %s
                    RETURNING patient_id, name, gender, birth_date, phone
                    ''', (patient.name, patient.gender, patient.birth_date, patient.phone, patient_id)
                )
                row = cur.fetchone()
                return {"patient_id": row[0], "name": row[1], "gender": row[2], "birth_date": row[3], "phone": row[4]}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    
@router.delete("/{patient_id}")
async def delete_patient(patient_id: int):
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                check_exists("patients", "patient_id", patient_id)
                cur.execute(
                    "SELECT 1 FROM appointments WHERE patient_id = %s", (patient_id,)
                )
                has_appointment = cur.fetchone()
                if has_appointment:
                    raise HTTPException(status_code=404, detail="Cannot delete patient with existing appointments")
                cur.execute(
                    "DELETE FROM patients WHERE patient_id = %s", (patient_id,)
                )
                return {"message": f"Patient with id {patient_id} has been deleted successfully"}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    
@router.get("/{id}/history", response_model=HistoryPatient)
async def get_patient_history(id: int):
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                check_exists("patients", "patient_id", id)
                cur.execute('''
                    SELECT p.patient_id, p.name,
                           a.appointment_id, d.name, d.specialty,
                           a.appointment_date, a.status,
                           pr.medicine, pr.dosage
                    FROM patients p
                    JOIN appointments a ON p.patient_id = a.patient_id
                    JOIN doctors d ON d.doctor_id = a.doctor_id
                    JOIN prescriptions pr ON pr.appointment_id = a.appointment_id
                    WHERE p.patient_id = %s
                    ORDER BY a.appointment_id
                    ''', (id,)
                )
                rows = cur.fetchall()
                if not rows:
                    raise HTTPException(status_code=404, detail=f"Patient with no history")
                patient_id, name = rows[0][0], rows[0][1]
                appointments_dict = {}
                for row in rows:
                    appt_id = row[2]
                    if appt_id not in appointments_dict:
                        appointments_dict[appt_id] = {
                            "appointment_id": appt_id,
                            "doctor": row[3],
                            "specialty": row[4],
                            "appointment_date": row[5],
                            "status": row[6],
                            "prescriptions": []
                        }
                    appointments_dict[appt_id]["prescriptions"].append({
                        "medicine": row[7],
                        "dosage": row[8] 
                    })
                appointments = list(appointments_dict.values())
                return {
                    "patient_id": patient_id,
                    "name": name,
                    "appointments": appointments
                }
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")