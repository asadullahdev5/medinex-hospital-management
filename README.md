# 🏥 Hospital Management System — FastAPI

A modern, modular **Hospital Management System (HMS)** built with FastAPI and Python. The project aims to simplify hospital operations through a centralized dashboard for patient management, doctor appointments, emergency cases, ambulance tracking, OPD schedules, and bed availability.

## ✨ Features

### 📊 Hospital Dashboard
- Centralized dashboard for hospital operations.
- Hospital profile, contact details, and hospital image.
- Overview of appointments, emergency cases, doctors, and patients.
- Real-time operational statistics with automatic dashboard refresh.

### 🔐 Authentication & User Management
- User registration and login.
- Role-based access for patients, doctors, and administrators.
- Secure password hashing and token-based authentication.
- Admin controls for managing users and hospital operations.

### 👨‍⚕️ Doctor Management
- Doctor profiles and specializations.
- Department-wise doctor directory.
- Consultation fees and availability.
- Doctor schedule management.

### 📅 Appointment Management
- Book appointments with available doctors.
- View and manage appointment schedules.
- Cancel or update appointments.
- Track appointment status.

### 🚨 Emergency Management
- Track daily emergency cases.
- Classify cases by severity: Critical, Urgent, and Stable.
- Monitor case status, including Waiting, Under Treatment, and Admitted.
- Associate emergency cases with ambulances and hospital departments.

### 🚑 Ambulance Management
- Maintain ambulance fleet records.
- Track ambulance availability and operational status.
- Manage Available, On Duty, and Maintenance statuses.
- Link ambulances to emergency cases.

### 🏥 OPD & Department Management
- Manage hospital departments and outpatient services.
- Configure department-wise OPD timings.
- Display operating days and opening hours.
- Determine whether an OPD is currently open or closed.

### 🛏️ Ward & Bed Management
- Track general ward, ICU, and CCU beds.
- Monitor available and occupied beds.
- View bed availability by ward.
- Support patient admission and bed allocation workflows.

## 🛠️ Technology Stack

- **Backend:** Python, FastAPI
- **API Documentation:** Swagger UI, OpenAPI
- **Database:** PostgreSQL
- **Testing:** Pytest, SQLite for supported tests
- **Server:** Uvicorn
- **Containerization:** Docker and Docker Compose
- **Frontend:** HTML, CSS, JavaScript
- **Authentication:** JWT-based authentication and password hashing

## 📁 Project Structure

```text
hospital-management-system/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── doctors.py
│   │   ├── appointments.py
│   │   ├── admin.py
│   │   ├── emergency.py
│   │   ├── ambulances.py
│   │   ├── departments.py
│   │   └── beds.py
│   └── static/
│       └── index.html
├── tests/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

*Note: The structure above represents the intended modular architecture. Adjust it to match the files actually implemented in your repository.*

## ⚙️ Getting Started

### 1. Clone the repository

```powershell
git clone <YOUR_REPOSITORY_URL>
cd hospital-management-system
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the environment again.

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example` and configure the required settings.

```env
DATABASE_URL=your_database_connection_string
SECRET_KEY=replace_with_a_long_random_secret
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=replace_with_a_strong_password
```

Never commit your real `.env` file, database credentials, or secret keys to GitHub.

### 5. Start the database

If the project uses PostgreSQL through Docker Compose:

```powershell
docker compose up -d db
```

Ensure the database connection settings match your local configuration.

### 6. Run the application

```powershell
uvicorn app.main:app --reload
```

### 7. Open the application

| Resource | URL |
|---|---|
| Hospital Dashboard | http://127.0.0.1:8000/ |
| Interactive API Docs | http://127.0.0.1:8000/docs |
| OpenAPI Schema | http://127.0.0.1:8000/openapi.json |

*These URLs assume the application serves the frontend at `/` and exposes the standard FastAPI documentation routes.*

## 🧪 Running Tests

Run the test suite using:

```powershell
pytest -q
```

Tests should verify authentication, appointment workflows, database operations, and hospital management endpoints. SQLite can be used for isolated tests when the application supports a separate test database configuration.

## 🗺️ Development Roadmap

- [x] FastAPI application foundation
- [x] Initial authentication and appointment workflow
- [x] Basic web interface
- [ ] Complete hospital operations dashboard
- [ ] Advanced patient registration and medical records
- [ ] Emergency case management and triage
- [ ] Ambulance fleet and dispatch management
- [ ] Department-wise OPD schedules
- [ ] Ward, ICU, and CCU bed management
- [ ] Role-based permissions across all modules
- [ ] Reporting and analytics
- [ ] Docker-based production deployment
- [ ] Automated testing and CI/CD

*Update the checklist as each feature is implemented and tested.*

## 🔒 Security & Privacy

- Store passwords using a secure password-hashing algorithm.
- Keep secrets and credentials in environment variables.
- Enforce authorization checks on protected endpoints.
- Validate user input and handle errors safely.
- Use HTTPS and secure deployment settings in production.
- Avoid using real patient records in development or demonstration environments.

## 🎯 Project Goals

The goal is to develop a scalable, maintainable hospital management platform that brings essential hospital workflows into one system. The project is being developed as a practical backend engineering portfolio project, with an emphasis on REST APIs, authentication, database design, testing, and modular architecture.

## ⚠️ Disclaimer

This project is intended for educational and development purposes. It is not a certified clinical system and should not be used for real emergency dispatch, patient care decisions, or production patient data without appropriate security, reliability, privacy, and clinical validation.

## 👨‍💻 Author

**Asad Ullah**

Computer Science Undergraduate | Python & Backend Development

- GitHub: [@asadullahdev5](https://github.com/asadullahdev5)
- LinkedIn: [Asad Ullah](https://linkedin.com/in/asad-ullahdev)

---

*Built with Python and FastAPI, with the goal of making hospital operations more organized, accessible, and efficient.*
