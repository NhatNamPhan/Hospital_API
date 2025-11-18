# Hospital_API

Tài liệu nhanh về project Hospital_API (FastAPI) — bao gồm các endpoint, cách cấu hình và chạy.

**Yêu cầu**

- Python 3.10+
- PostgreSQL
- Các package trong `requirements.txt` (cài bằng `pip install -r requirements.txt`)

**Chuẩn bị database**

1. Khởi động PostgreSQL.
2. Tạo database và import schema:

```powershell
psql -h localhost -U postgres -c "CREATE DATABASE hospital_db;"
psql -h localhost -U postgres -d hospital_db -f hospital_db.sql
```

**Cài dependencies & chạy ứng dụng**

```powershell
cd E:\Python\DataEngineer\Python\Hospital_API
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload 
```

Mở Swagger UI: `http://127.0.0.1:8000/docs`

---

**Endpoints (tổng quan)**

Lưu ý: dưới đây là danh sách endpoint được document; các endpoint tương ứng với router trong `app/routers`.

**Endpoint Patients**

- POST /patients
  - Body (JSON): `{ "name": "", "gender": "M|F", "birth_date": "YYYY-MM-DD", "phone": "" }`
  - Trả về: `{"message": "Patient added successfully", "patient_id": <id>}`
- GET /patients
  - Trả về: list các patient (mảng object)
- GET /patients/{id}
  - Trả về: object patient theo `id`
- PUT /patients/{id}
  - Body (JSON): như POST
  - Trả về: object patient đã cập nhật
- DELETE /patients/{id}
  - Xóa patient (nếu không có appointment liên quan)
- GET /patients/history/{id}
  - (Nếu bạn muốn) endpoint này chưa được triển khai mặc định — có thể dùng để trả lịch sử thay đổi/appointment của patient.

**Endpoint Doctors**

- POST /doctors
  - Body: `{ "name": "", "specialty": "" }`
- GET /doctors
  - Trả về: list các doctors
- GET /doctors/stats
  - (Tùy chọn) chưa triển khai mặc định — có thể dùng để trả thống kê (số appointment, v.v.)
- GET /doctors/{id}
  - Trả về: doctor theo id
- PUT /doctors/{id}
  - Cập nhật doctor
- DELETE /doctors/{id}

**Endpoint Appointments**

- POST /appointments
  - Body: `{ "patient_id": <int>, "doctor_id": <int>, "appointment_date": "YYYY-MM-DD" }`
- GET /appointments
  - Trả về: list các appointment
- PUT /appointments/status/{id}
  - Body: `{ "status": "scheduled|cancelled|done" }` — cập nhật trạng thái
- GET /appointments/{id}/prescription
  - Trả về: prescription(s) cho appointment (hoặc danh sách rỗng nếu chưa có)

**Endpoint Prescriptions**

- POST /prescriptions
  - Body: `{ "appointment_id": <int>, "medicine": "", "dosage": "" }`

---

