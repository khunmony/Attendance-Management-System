"""Import every model so Base.metadata (and Alembic) sees all tables."""
from app.models.academic import AcademicYear, Enrollment, SchoolClass, Term
from app.models.attendance import AttendanceRecord
from app.models.course import Course, ScheduleSlot, Subject
from app.models.excuse import AbsenceExcuse
from app.models.session import ClassSession, QrToken
from app.models.settings import Holiday, SchoolLocation, SchoolSetting
from app.models.system import AuditLog, Notification
from app.models.user import RefreshToken, User

__all__ = [
    "AbsenceExcuse", "AcademicYear", "AttendanceRecord", "AuditLog", "ClassSession",
    "Course", "Enrollment", "Holiday", "Notification", "QrToken", "RefreshToken",
    "ScheduleSlot", "SchoolClass", "SchoolLocation", "SchoolSetting", "Subject",
    "Term", "User",
]
