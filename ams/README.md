# School Attendance Management System (AMS)

Backend: FastAPI + SQLAlchemy + PostgreSQL. Frontend: plain HTML/CSS/JavaScript.
Roles: **ADMIN**, **TEACHER**, **STUDENT**.

## Quick start

```bash
# 1. Configuration
cp .env.example .env

# 2. Start PostgreSQL (needs Docker)
docker compose up -d

# 3. Install and run the API
cd backend
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

alembic revision --autogenerate -m "initial schema"   # first time only, then commit the file
alembic upgrade head
python -m scripts.seed                                 # creates settings + first admin
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs  |  Tests: `pytest` (runs on in-memory SQLite)

Serve the frontend with any static server, e.g. `cd frontend && python -m http.server 5500`.

## Layout

- `backend/app/models` - SQLAlchemy tables (reference design in `docs/schema.prisma`)
- `backend/app/api/v1/endpoints` - thin route handlers
- `backend/app/services` - business logic (attendance status rules, QR, excuses, reports)
- `backend/alembic` - database migrations
- `frontend/` - static pages

## Next steps

Implement the endpoints and `attendance_service.py` (Present / Late / Absent rules).
