CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    birth_date DATE,
    phone VARCHAR(15)
);

CREATE TABLE doctors (
    doctor_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100)
);

CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id),
    doctor_id INT REFERENCES doctors(doctor_id),
    appointment_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled'
);

CREATE TABLE prescriptions (
    prescription_id SERIAL PRIMARY KEY,
    appointment_id INT REFERENCES appointments(appointment_id),
    medicine VARCHAR(100),
    dosage VARCHAR(50)
);


ALTER TABLE appointments 
ADD CONSTRAINT check_status CHECK (status IN ('scheduled', 'done', 'canceled'));
