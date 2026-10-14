# app/routers/admin.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import require_role
from app.database import get_db

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(require_role("admin"))])


@router.get("/users", response_model=List[schemas.UserResponse])
def all_users(db: Session = Depends(get_db)):
    return db.query(models.User).order_by(models.User.id).all()


@router.get("/appointments", response_model=List[schemas.AppointmentResponse])
def all_appointments(db: Session = Depends(get_db)):
    return db.query(models.Appointment).order_by(models.Appointment.id).all()


@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    users = dict(db.query(models.User.role, func.count()).group_by(models.User.role).all())
    appts = dict(db.query(models.Appointment.status, func.count()).group_by(models.Appointment.status).all())
    return {"users_by_role": users, "appointments_by_status": appts}


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), admin: models.User = Depends(require_role("admin"))):
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="Apna account delete nahi kar sakte")
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User nahi mila")
    if db.query(models.Appointment).filter(
        (models.Appointment.patient_id == user_id) | (models.Appointment.doctor_id == user_id)
    ).first():
        raise HTTPException(status_code=400, detail="Is user ki appointments hain, delete nahi ho sakta")
    db.delete(user)
    db.commit()
