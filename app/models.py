from pydantic import BaseModel
from datetime import date
from typing import List

class Patient(BaseModel):
    name: str
    gender: str | None = None
    birth_date: date | None = None
    phone: str | None = None

class Doctor(BaseModel):
    name: str
    specialty: str

class AppointmentIn(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date

class AppointmentOut(BaseModel):
    appointment_id: int
    patient: str
    doctor: str
    appointment_date: date
    status: str

class AppointmentUpdateStatus(BaseModel):
    status: str
    
class Prescription(BaseModel):
    appointment_id: int
    medicine: str
    dosage: str