from fastapi import FastAPI
from app.routers import patients, doctors, appointments, prescriptions

app = FastAPI(title='Hospital Management API')

app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
# app.include_router(prescriptions.router)