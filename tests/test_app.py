# tests/test_app.py
from datetime import date, timedelta
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app, hash_password
from app import models

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = TestingSession()
    db.add(models.User(name="Admin", email="admin@t.com", hashed_password=hash_password("admin123"), role="admin"))
    db.commit()
    db.close()
    return TestClient(app)


def signup(c, name, email, role):
    return c.post("/auth/signup", json={"name": name, "email": email, "password": "secret123", "role": role})


def login(c, email, password="secret123"):
    r = c.post("/auth/login", data={"username": email, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def next_weekday(weekday):
    d = date.today() + timedelta(days=1)
    while d.weekday() != weekday:
        d += timedelta(days=1)
    return d


def test_signup_login_me(client):
    assert signup(client, "Ali", "ali@t.com", "patient").status_code == 201
    assert signup(client, "Ali", "ali@t.com", "patient").status_code == 400
    h = login(client, "ali@t.com")
    assert client.get("/auth/me", headers=h).json()["email"] == "ali@t.com"
    assert client.post("/auth/login", data={"username": "ali@t.com", "password": "wrong"}).status_code == 401


def test_cannot_signup_as_admin(client):
    assert signup(client, "Hack", "h@t.com", "admin").status_code == 422


def test_full_booking_flow(client):
    signup(client, "Dr Sara", "sara@t.com", "doctor")
    signup(client, "Ali", "ali@t.com", "patient")
    dh, ph = login(client, "sara@t.com"), login(client, "ali@t.com")
    doctor_id = client.get("/doctors/").json()[0]["id"]

    # patient schedule nahi bana sakta
    body = {"day_of_week": "Monday", "start_time": "09:00", "end_time": "13:00"}
    assert client.post("/doctors/schedule", json=body, headers=ph).status_code == 403
    assert client.post("/doctors/schedule", json=body, headers=dh).status_code == 201
    assert client.post("/doctors/schedule", json=body, headers=dh).status_code == 400  # overlap

    monday = next_weekday(0).isoformat()
    book = {"doctor_id": doctor_id, "appointment_date": monday, "appointment_time": "10:00"}
    r = client.post("/appointments/", json=book, headers=ph)
    assert r.status_code == 201, r.text
    appt_id = r.json()["id"]

    assert client.post("/appointments/", json=book, headers=ph).status_code == 409  # slot taken
    book["appointment_time"] = "15:00"
    assert client.post("/appointments/", json=book, headers=ph).status_code == 400  # schedule se bahar
    tuesday = {"doctor_id": doctor_id, "appointment_date": next_weekday(1).isoformat(), "appointment_time": "10:00"}
    assert client.post("/appointments/", json=tuesday, headers=ph).status_code == 400

    assert len(client.get("/appointments/my", headers=ph).json()) == 1
    assert len(client.get("/appointments/my", headers=dh).json()) == 1

    assert client.patch(f"/appointments/{appt_id}/cancel", headers=ph).json()["status"] == "cancelled"
    # cancel ke baad slot dobara book ho sakta hai
    book["appointment_time"] = "10:00"
    assert client.post("/appointments/", json=book, headers=ph).status_code == 201


def test_admin_only(client):
    signup(client, "Ali", "ali@t.com", "patient")
    assert client.get("/admin/users", headers=login(client, "ali@t.com")).status_code == 403
    ah = login(client, "admin@t.com", "admin123")
    assert len(client.get("/admin/users", headers=ah).json()) == 2
    assert "users_by_role" in client.get("/admin/stats", headers=ah).json()
