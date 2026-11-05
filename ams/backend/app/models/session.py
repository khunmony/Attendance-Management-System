import uuid
import datetime as dt
from datetime import datetime, time

from sqlalchemy import Date, DateTime, Index, String, Time, UniqueConstraint, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.academic import SchoolClass
from app.models.course import Course
from app.models.enums import SessionStatus
from app.models.mixins import UUIDPrimaryKey, fk
from app.models.user import User


class ClassSession(UUIDPrimaryKey, Base):
    """One concrete class meeting. course_id is NULL for a daily homeroom session."""

    __tablename__ = "class_sessions"
    __table_args__ = (
        # NULLS NOT DISTINCT (PostgreSQL 15+) so two homeroom sessions
        # (course_id NULL) can't be created for the same class/date/time.
        UniqueConstraint(
            "class_id", "course_id", "date", "start_time",
            postgresql_nulls_not_distinct=True,
        ),
        Index("ix_class_sessions_teacher_id_date", "teacher_id", "date"),
    )

    class_id: Mapped[uuid.UUID] = fk("classes.id")
    course_id: Mapped[uuid.UUID | None] = fk("courses.id", ondelete="SET NULL")
    teacher_id: Mapped[uuid.UUID] = fk("users.id", ondelete="RESTRICT")
    date: Mapped[dt.date] = mapped_column(Date, index=True)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    status: Mapped[SessionStatus] = mapped_column(
        SAEnum(SessionStatus, name="session_status"), default=SessionStatus.SCHEDULED
    )
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    school_class: Mapped[SchoolClass] = relationship()
    course: Mapped[Course | None] = relationship()
    teacher: Mapped[User] = relationship(foreign_keys=[teacher_id])


class QrToken(UUIDPrimaryKey, Base):
    """Short-lived token the teacher shows as a QR code for one session."""

    __tablename__ = "qr_tokens"

    session_id: Mapped[uuid.UUID] = fk("class_sessions.id")
    token_hash: Mapped[str] = mapped_column(String(255), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
