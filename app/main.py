# app/main.py
import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from app import models  # noqa: F401  (tables register hone ke liye zaroori)
from app.auth import hash_password
from app.database import Base, SessionLocal, engine
from app.routers import admin, appointments, auth, doctors


def seed_admin():
    email, password = os.getenv("ADMIN_EMAIL"), os.getenv("ADMIN_PASSWORD")
    if not email or not password:
        return
    db = SessionLocal()
    try:
        if not db.query(models.User).filter(models.User.email == email.lower()).first():
            db.add(models.User(name="Admin", email=email.lower(),
                               hashed_password=hash_password(password), role="admin"))
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        seed_admin()
    except Exception as exc:
        raise RuntimeError(
            "Database se connect nahi ho saka. 'docker compose up -d db' chalao "
            f"ya .env mein DATABASE_URL check karo.\nAsal error: {exc}"
        ) from exc
    yield


app = FastAPI(
    title="Clinic Appointment Booking System",
    description="Backend API for Karachi Clinic Management",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(admin.router)


# Frontend (app/static/index.html) -> http://127.0.0.1:8000/app/
app.mount("/app", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="frontend")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/app/")
