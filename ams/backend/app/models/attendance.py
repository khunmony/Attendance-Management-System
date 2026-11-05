import uuid
import datetime as dt
from datetime import datetime

from sqlalchemy import Date, DateTime, Index, String, UniqueConstraint, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import AttendanceStatus, MarkMethod
from app.models.mixins import Timestamps, UUIDPrimaryKey, fk
from app.models.session import ClassSession
from app.models.user import User


class AttendanceRecord(UUIDPrimaryKey, Timestamps, Base):
    __tablename__ = "attendance_records"
    __table_args__ = (
        UniqueConstraint("session_id", "student_id"),
        Index("ix_attendance_records_student_id_date", "student_id", "date"),
        Index("ix_attendance_records_date_status", "date", "status"),
    )

    session_id: Mapped[uuid.UUID] = fk("class_sessions.id")
    student_id: Mapped[uuid.UUID] = fk("users.id")
    date: Mapped[dt.date] = mapped_column(Date)  # copied from the session for fast reports

    status: Mapped[AttendanceStatus] = mapped_column(
        SAEnum(AttendanceStatus, name="attendance_status"), default=AttendanceStatus.ABSENT
    )
    method: Mapped[MarkMethod] = mapped_column(
        SAEnum(MarkMethod, name="mark_method"), default=MarkMethod.TEACHER
    )
    check_in_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    late_minutes: Mapped[int] = mapped_column(default=0)
    note: Mapped[str | None] = mapped_column(String(500))

    marked_by_id: Mapped[uuid.UUID | None] = fk("users.id", ondelete="SET NULL")

    # Correction after the fact (teacher/admin)
    is_overridden: Mapped[bool] = mapped_column(default=False)
    override_reason: Mapped[str | None] = mapped_column(String(500))
    overridden_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    excuse_id: Mapped[uuid.UUID | None] = fk("absence_excuses.id", ondelete="SET NULL")

    session: Mapped[ClassSession] = relationship()
    student: Mapped[User] = relationship(foreign_keys=[student_id])
    marked_by: Mapped[User | None] = relationship(foreign_keys=[marked_by_id])
