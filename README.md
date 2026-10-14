# Clinic Booking System (FastAPI)

## Chalane ka tareeqa
```powershell
docker compose up -d db
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Docs: http://127.0.0.1:8000/docs  |  Admin login: `.env` mein ADMIN_EMAIL / ADMIN_PASSWORD

## Tests (DB ki zaroorat nahi, sqlite use hota hai)
```powershell
pytest -q
```
