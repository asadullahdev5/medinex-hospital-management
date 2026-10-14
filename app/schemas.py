# app/schemas.py
from datetime import time, date
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

Day = Literal["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# --- User ---
class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)
    role: Literal["patient", "doctor"] = "patient"  # admin signup se nahi banta


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


# --- Doctor schedule ---
class DoctorScheduleCreate(BaseModel):
    day_of_week: Day
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def check_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time start_time ke baad honi chahiye")
        return self


class DoctorScheduleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    doctor_id: int
    day_of_week: str
    start_time: time
    end_time: time


# --- Appointment ---
class AppointmentCreate(BaseModel):
    doctor_id: int
    appointment_date: date
    appointment_time: time


class AppointmentStatusUpdate(BaseModel):
    status: Literal["booked", "completed", "cancelled"]


class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    status: str
