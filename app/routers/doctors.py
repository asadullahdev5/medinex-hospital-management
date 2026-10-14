# app/routers/doctors.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import require_role
from app.database import get_db

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.get("/", response_model=List[schemas.UserResponse])
def list_doctors(db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.role == "doctor").all()


@router.get("/{doctor_id}/schedule", response_model=List[schemas.DoctorScheduleResponse])
def doctor_schedule(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(models.User).filter_by(id=doctor_id, role="doctor").first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor nahi mila")
    return db.query(models.DoctorSchedule).filter_by(doctor_id=doctor_id).all()


@router.post("/schedule", response_model=schemas.DoctorScheduleResponse, status_code=status.HTTP_201_CREATED)
def add_schedule(
    payload: schemas.DoctorScheduleCreate,
    db: Session = Depends(get_db),
    doctor: models.User = Depends(require_role("doctor")),
):
    clash = (
        db.query(models.DoctorSchedule)
        .filter(
            models.DoctorSchedule.doctor_id == doctor.id,
            models.DoctorSchedule.day_of_week == payload.day_of_week,
            models.DoctorSchedule.start_time < payload.end_time,
            models.DoctorSchedule.end_time > payload.start_time,
        )
        .first()
    )
    if clash:
        raise HTTPException(status_code=400, detail="Is din ka schedule overlap kar raha hai")
    sched = models.DoctorSchedule(doctor_id=doctor.id, **payload.model_dump())
    db.add(sched)
    db.commit()
    db.refresh(sched)
    return sched


@router.delete("/schedule/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    doctor: models.User = Depends(require_role("doctor")),
):
    sched = db.query(models.DoctorSchedule).filter_by(id=schedule_id, doctor_id=doctor.id).first()
    if not sched:
        raise HTTPException(status_code=404, detail="Schedule nahi mila")
    db.delete(sched)
    db.commit()
