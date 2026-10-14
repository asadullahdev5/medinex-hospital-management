# app/main.py
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth

# Database tables create karna
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Clinic Appointment Booking System",
    description="Backend API for Karachi Clinic Management",
    version="1.0.0"
)

# Routers include karna
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to Clinic Appointment Booking System API! 🏥"}