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

class DoctorStatistics(Doctor):
    total_appointment: int
    completed: int

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

class PrescriptionOut(BaseModel):
    prescription_id: int
    medicine: str
    dosage: str
    
class AppointmentDetailPrescription(BaseModel):
    appointment_id: int
    prescriptions: List[PrescriptionOut]

class PrescriptionOutNotId(BaseModel):
    medicine: str
    dosage: str

class ApptOut(BaseModel):
    appointment_id: int
    doctor: str
    specialty: str
    appointment_date: date
    status: str
    prescriptions: List[PrescriptionOutNotId]
    
class HistoryPatient(BaseModel):
    patient_id: int
    name: str
    appointments: List[ApptOut]

    