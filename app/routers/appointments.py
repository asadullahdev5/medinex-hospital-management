# app/routers/appointments.py
from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import get_current_user, require_role
from app.database import get_db

router = APIRouter(prefix="/appointments", tags=["Appointments"])

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


@router.post("/", response_model=schemas.AppointmentResponse, status_code=status.HTTP_201_CREATED)
def book_appointment(
    payload: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    patient: models.User = Depends(require_role("patient")),
):
    doctor = db.query(models.User).filter_by(id=payload.doctor_id, role="doctor").first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor nahi mila")

    if payload.appointment_date < date.today():
        raise HTTPException(status_code=400, detail="Guzri hui date par booking nahi ho sakti")

    day = DAYS[payload.appointment_date.weekday()]
    in_schedule = (
        db.query(models.DoctorSchedule)
        .filter(
            models.DoctorSchedule.doctor_id == doctor.id,
            models.DoctorSchedule.day_of_week == day,
            models.DoctorSchedule.start_time <= payload.appointment_time,
            models.DoctorSchedule.end_time > payload.appointment_time,
        )
        .first()
    )
    if not in_schedule:
        raise HTTPException(status_code=400, detail=f"Doctor {day} ko is waqt available nahi hai")

    taken = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.doctor_id == doctor.id,
            models.Appointment.appointment_date == payload.appointment_date,
            models.Appointment.appointment_time == payload.appointment_time,
            models.Appointment.status != "cancelled",
        )
        .first()
    )
    if taken:
        raise HTTPException(status_code=409, detail="Yeh slot pehle se book hai")

    appt = models.Appointment(patient_id=patient.id, **payload.model_dump())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt


@router.get("/my", response_model=List[schemas.AppointmentResponse])
def my_appointments(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    q = db.query(models.Appointment)
    if user.role == "patient":
        q = q.filter(models.Appointment.patient_id == user.id)
    elif user.role == "doctor":
        q = q.filter(models.Appointment.doctor_id == user.id)
    return q.order_by(models.Appointment.appointment_date, models.Appointment.appointment_time).all()


@router.patch("/{appointment_id}/cancel", response_model=schemas.AppointmentResponse)
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    appt = db.get(models.Appointment, appointment_id)
    if not appt or user.role not in ("admin",) and user.id not in (appt.patient_id, appt.doctor_id):
        raise HTTPException(status_code=404, detail="Appointment nahi mili")
    if appt.status != "booked":
        raise HTTPException(status_code=400, detail=f"Appointment already {appt.status} hai")
    appt.status = "cancelled"
    db.commit()
    db.refresh(appt)
    return appt


@router.patch("/{appointment_id}/status", response_model=schemas.AppointmentResponse)
def update_status(
    appointment_id: int,
    payload: schemas.AppointmentStatusUpdate,
    db: Session = Depends(get_db),
    doctor: models.User = Depends(require_role("doctor")),
):
    appt = db.query(models.Appointment).filter_by(id=appointment_id, doctor_id=doctor.id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment nahi mili")
    appt.status = payload.status
    db.commit()
    db.refresh(appt)
    return appt
