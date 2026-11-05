from fastapi import APIRouter

from app.api.v1.endpoints import (
    attendance, auth, classes, courses, excuses, holidays,
    notifications, reports, sessions, settings, users,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(classes.router, prefix="/classes", tags=["classes"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(excuses.router, prefix="/excuses", tags=["excuses"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(holidays.router, prefix="/holidays", tags=["holidays"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
