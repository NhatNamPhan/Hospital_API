from fastapi import APIRouter, HTTPException
from app.models import Prescription
from app.database import get_db
from app.utils import check_exists
import psycopg2


router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])

@router.post("")
async def add_prescription(presc: Prescription):
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                check_exists("appointments", "appointment_id", presc.appointment_id)
                cur.execute(
                    "INSERT INTO prescriptions VALUES (%s, %s, %s) RETURNING prescription_id",
                    (presc.appointment_id, presc.medicine, presc.dosage)
                )
                new_id = cur.fetchone()
                return {"message": "Prescription added successfully", "prescription_id": new_id}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
