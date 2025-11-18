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



-- Insert 15 patients (ít patients nhưng mỗi người khám nhiều lần)
INSERT INTO patients (name, gender, birth_date, phone) VALUES
('John Smith', 'Male', '1985-03-15', '1234567890'),
('Emily Johnson', 'Female', '1990-07-22', '2345678901'),
('Michael Brown', 'Male', '1978-11-30', '3456789012'),
('Sarah Davis', 'Female', '1982-05-18', '4567890123'),
('David Wilson', 'Male', '1995-09-08', '5678901234'),
('Jennifer Miller', 'Female', '1988-12-25', '6789012345'),
('Robert Taylor', 'Male', '1975-02-14', '7890123456'),
('Lisa Anderson', 'Female', '1992-06-19', '8901234567'),
('William Martinez', 'Male', '1980-04-03', '9012345678'),
('Jessica Thomas', 'Female', '1987-08-11', '1122334455'),
('Christopher Lee', 'Male', '1993-01-28', '2233445566'),
('Amanda White', 'Female', '1979-10-07', '3344556677'),
('Daniel Harris', 'Male', '1984-03-22', '4455667788'),
('Michelle Clark', 'Female', '1991-07-15', '5566778899'),
('Matthew Lewis', 'Male', '1976-12-08', '6677889900');

-- Insert 10 doctors (ít doctors nhưng mỗi người có nhiều appointment)
INSERT INTO doctors (name, specialty) VALUES
('Dr. Robert Johnson', 'Cardiology'),
('Dr. Susan Williams', 'Pediatrics'),
('Dr. Richard Jones', 'Dermatology'),
('Dr. Patricia Brown', 'Neurology'),
('Dr. Charles Davis', 'Orthopedics'),
('Dr. Karen Miller', 'Oncology'),
('Dr. Christopher Wilson', 'Psychiatry'),
('Dr. Nancy Taylor', 'Endocrinology'),
('Dr. Thomas Anderson', 'Gastroenterology'),
('Dr. Lisa Martinez', 'Rheumatology');

-- Insert 50 appointments (mỗi patient khám nhiều lần, mỗi doctor có nhiều appointment)
INSERT INTO appointments (patient_id, doctor_id, appointment_date, status) VALUES
-- Patient 1 (John Smith) khám nhiều lần với Dr. Robert Johnson (Cardiology)
(1, 1, '2024-01-05', 'done'),
(1, 1, '2024-02-10', 'done'),
(1, 1, '2024-03-15', 'scheduled'),

-- Patient 2 (Emily Johnson) khám với nhiều doctors khác nhau
(2, 2, '2024-01-10', 'done'),
(2, 1, '2024-02-12', 'done'),
(2, 3, '2024-03-18', 'canceled'),

-- Patient 3 (Michael Brown) khám thường xuyên
(3, 4, '2024-01-08', 'done'),
(3, 4, '2024-02-14', 'done'),
(3, 4, '2024-03-20', 'scheduled'),
(3, 5, '2024-01-25', 'done'),

-- Patient 4 (Sarah Davis) 
(4, 6, '2024-01-12', 'done'),
(4, 6, '2024-02-18', 'done'),
(4, 7, '2024-03-22', 'scheduled'),

-- Patient 5 (David Wilson)
(5, 8, '2024-01-15', 'done'),
(5, 8, '2024-02-20', 'done'),
(5, 9, '2024-03-25', 'canceled'),

-- Patient 6 (Jennifer Miller)
(6, 10, '2024-01-18', 'done'),
(6, 1, '2024-02-22', 'done'),
(6, 2, '2024-03-28', 'scheduled'),

-- Patient 7 (Robert Taylor)
(7, 3, '2024-01-20', 'done'),
(7, 4, '2024-02-25', 'done'),
(7, 5, '2024-04-01', 'scheduled'),

-- Patient 8 (Lisa Anderson)
(8, 6, '2024-01-22', 'done'),
(8, 7, '2024-02-28', 'done'),
(8, 8, '2024-04-03', 'scheduled'),

-- Patient 9 (William Martinez)
(9, 9, '2024-01-25', 'done'),
(9, 10, '2024-03-02', 'done'),
(9, 1, '2024-04-05', 'scheduled'),

-- Patient 10 (Jessica Thomas)
(10, 2, '2024-01-28', 'done'),
(10, 3, '2024-03-05', 'done'),
(10, 4, '2024-04-08', 'canceled'),

-- Patient 11 (Christopher Lee)
(11, 5, '2024-02-01', 'done'),
(11, 6, '2024-03-08', 'done'),
(11, 7, '2024-04-10', 'scheduled'),

-- Patient 12 (Amanda White)
(12, 8, '2024-02-03', 'done'),
(12, 9, '2024-03-10', 'done'),
(12, 10, '2024-04-12', 'scheduled'),

-- Patient 13 (Daniel Harris)
(13, 1, '2024-02-05', 'done'),
(13, 2, '2024-03-12', 'done'),
(13, 3, '2024-04-14', 'scheduled'),

-- Patient 14 (Michelle Clark)
(14, 4, '2024-02-08', 'done'),
(14, 5, '2024-03-15', 'done'),
(14, 6, '2024-04-16', 'scheduled'),

-- Patient 15 (Matthew Lewis)
(15, 7, '2024-02-10', 'done'),
(15, 8, '2024-03-18', 'done'),
(15, 9, '2024-04-18', 'scheduled'),

-- Thêm một số appointments để đủ 50
(1, 2, '2024-04-20', 'scheduled'),
(2, 4, '2024-04-22', 'scheduled'),
(3, 6, '2024-04-24', 'scheduled'),
(4, 8, '2024-04-26', 'scheduled'),
(5, 10, '2024-04-28', 'scheduled');

-- Insert 50 prescriptions (mỗi appointment done thường có prescription)
INSERT INTO prescriptions (appointment_id, medicine, dosage) VALUES
-- Prescriptions cho John Smith (patient 1)
(1, 'Amoxicillin', '500mg three times daily'),
(1, 'Ibuprofen', '400mg every 6 hours'),
(2, 'Lisinopril', '10mg once daily'),
(2, 'Atorvastatin', '20mg at bedtime'),

-- Prescriptions cho Emily Johnson (patient 2)
(4, 'Metformin', '500mg twice daily'),
(5, 'Levothyroxine', '50mcg every morning'),

-- Prescriptions cho Michael Brown (patient 3)
(7, 'Albuterol', '2 puffs every 4-6 hours'),
(7, 'Omeprazole', '20mg once daily'),
(8, 'Sertraline', '50mg once daily'),
(9, 'Simvastatin', '40mg at bedtime'),

-- Prescriptions cho Sarah Davis (patient 4)
(11, 'Losartan', '50mg once daily'),
(12, 'Gabapentin', '300mg three times daily'),

-- Prescriptions cho David Wilson (patient 5)
(14, 'Hydrochlorothiazide', '25mg once daily'),
(15, 'Metoprolol', '50mg twice daily'),

-- Prescriptions cho Jennifer Miller (patient 6)
(17, 'Warfarin', '5mg once daily'),
(18, 'Citalopram', '20mg once daily'),

-- Prescriptions cho Robert Taylor (patient 7)
(19, 'Tramadol', '50mg every 6 hours'),
(20, 'Pantoprazole', '40mg once daily'),

-- Prescriptions cho Lisa Anderson (patient 8)
(22, 'Amlodipine', '5mg once daily'),
(23, 'Fluoxetine', '20mg once daily'),

-- Prescriptions cho William Martinez (patient 9)
(25, 'Furosemide', '40mg once daily'),
(26, 'Clonazepam', '0.5mg twice daily'),

-- Prescriptions cho Jessica Thomas (patient 10)
(28, 'Trazodone', '50mg at bedtime'),
(29, 'Carvedilol', '6.25mg twice daily'),

-- Prescriptions cho Christopher Lee (patient 11)
(31, 'Allopurinol', '300mg once daily'),
(32, 'Duloxetine', '30mg once daily'),

-- Prescriptions cho Amanda White (patient 12)
(34, 'Pregabalin', '75mg twice daily'),
(35, 'Spironolactone', '25mg once daily'),

-- Prescriptions cho Daniel Harris (patient 13)
(37, 'Quetiapine', '25mg at bedtime'),
(38, 'Montelukast', '10mg at bedtime'),

-- Prescriptions cho Michelle Clark (patient 14)
(40, 'Escitalopram', '10mg once daily'),
(41, 'Venlafaxine', '75mg once daily'),

-- Prescriptions cho Matthew Lewis (patient 15)
(43, 'Buspirone', '10mg twice daily'),
(44, 'Cyclobenzaprine', '10mg three times daily'),

-- Thêm prescriptions cho các appointments khác
(3, 'Meloxicam', '15mg once daily'),
(6, 'Naproxen', '500mg twice daily'),
(10, 'Topiramate', '25mg twice daily'),
(13, 'Zolpidem', '10mg at bedtime'),
(16, 'Hydrocodone', '5mg every 6 hours'),
(21, 'Oxycodone', '5mg every 6 hours'),
(24, 'Prednisone', '20mg once daily'),
(27, 'Diazepam', '5mg every 8 hours'),
(30, 'Lorazepam', '1mg every 8 hours'),
(33, 'Clonidine', '0.1mg twice daily'),
(36, 'Doxazosin', '4mg once daily'),
(39, 'Finasteride', '5mg once daily'),
(42, 'Tamsulosin', '0.4mg at bedtime'),
(45, 'Memantine', '10mg twice daily'),
(46, 'Donepezil', '5mg at bedtime'),
(47, 'Rivastigmine', '3mg twice daily'),
(48, 'Galantamine', '8mg twice daily'),
(49, 'Carbidopa/Levodopa', '25/100mg three times daily'),
(50, 'Pramipexole', '0.125mg three times daily');
