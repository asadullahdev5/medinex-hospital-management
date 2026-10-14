# app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import time, date
from typing import Optional

# --- User Schemas ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "patient"  # patient, doctor, admin

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

# --- Token Schema ---
class Token(BaseModel):
    access_token: str
    token_type: str

# --- Doctor Schedule Schemas ---
class DoctorScheduleCreate(BaseModel):
    day_of_week: str  # e.g., "Monday"
    start_time: time
    end_time: time

class DoctorScheduleResponse(BaseModel):
    id: int
    doctor_id: int
    day_of_week: str
    start_time: time
    end_time: time

    class Config:
        from_attributes = True

# --- Appointment Schemas ---
class AppointmentCreate(BaseModel):
    doctor_id: int
    appointment_date: date
    appointment_time: time

class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    status: str

    class Config:
        from_attributes = True