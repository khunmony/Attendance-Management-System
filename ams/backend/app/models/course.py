import uuid
from datetime import time

from sqlalchemy import String, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.academic import SchoolClass
from app.models.mixins import UUIDPrimaryKey, fk
from app.models.user import User


class Subject(UUIDPrimaryKey, Base):
    __tablename__ = "subjects"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    code: Mapped[str] = mapped_column(String(20), unique=True)


class Course(UUIDPrimaryKey, Base):
    """A subject taught to a class by one teacher."""

    __tablename__ = "courses"
    __table_args__ = (UniqueConstraint("class_id", "subject_id"),)

    class_id: Mapped[uuid.UUID] = fk("classes.id")
    subject_id: Mapped[uuid.UUID] = fk("subjects.id")
    teacher_id: Mapped[uuid.UUID] = fk("users.id", ondelete="RESTRICT", index=True)

    school_class: Mapped[SchoolClass] = relationship()
    subject: Mapped[Subject] = relationship()
    teacher: Mapped[User] = relationship(foreign_keys=[teacher_id])


class ScheduleSlot(UUIDPrimaryKey, Base):
    """Weekly recurring timetable entry; ClassSessions are generated from these."""

    __tablename__ = "schedule_slots"
    __table_args__ = (UniqueConstraint("course_id", "day_of_week", "start_time"),)

    course_id: Mapped[uuid.UUID] = fk("courses.id")
    day_of_week: Mapped[int]  # 0=Sun ... 6=Sat
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)

    course: Mapped[Course] = relationship()
