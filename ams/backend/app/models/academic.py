import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Index, String, UniqueConstraint, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import EnrollmentStatus
from app.models.mixins import UUIDPrimaryKey, fk
from app.models.user import User


class AcademicYear(UUIDPrimaryKey, Base):
    __tablename__ = "academic_years"

    name: Mapped[str] = mapped_column(String(20), unique=True)  # "2026-2027"
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    is_current: Mapped[bool] = mapped_column(default=False)


class Term(UUIDPrimaryKey, Base):
    __tablename__ = "terms"
    __table_args__ = (UniqueConstraint("academic_year_id", "name"),)

    academic_year_id: Mapped[uuid.UUID] = fk("academic_years.id")
    name: Mapped[str] = mapped_column(String(50))  # "Term 1"
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)


class SchoolClass(UUIDPrimaryKey, Base):
    """A group of students, e.g. "Grade 10-A" in one academic year."""

    __tablename__ = "classes"
    __table_args__ = (UniqueConstraint("academic_year_id", "name"),)

    academic_year_id: Mapped[uuid.UUID] = fk("academic_years.id")
    name: Mapped[str] = mapped_column(String(100))
    grade_level: Mapped[int | None]
    homeroom_teacher_id: Mapped[uuid.UUID | None] = fk(
        "users.id", ondelete="SET NULL", index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    academic_year: Mapped[AcademicYear] = relationship()
    homeroom_teacher: Mapped[User | None] = relationship(foreign_keys=[homeroom_teacher_id])


class Enrollment(UUIDPrimaryKey, Base):
    __tablename__ = "enrollments"
    __table_args__ = (
        UniqueConstraint("student_id", "class_id"),
        Index("ix_enrollments_class_id_status", "class_id", "status"),
    )

    student_id: Mapped[uuid.UUID] = fk("users.id")
    class_id: Mapped[uuid.UUID] = fk("classes.id")
    status: Mapped[EnrollmentStatus] = mapped_column(
        SAEnum(EnrollmentStatus, name="enrollment_status"), default=EnrollmentStatus.ACTIVE
    )
    enrolled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    left_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    student: Mapped[User] = relationship(foreign_keys=[student_id])
    school_class: Mapped[SchoolClass] = relationship()
