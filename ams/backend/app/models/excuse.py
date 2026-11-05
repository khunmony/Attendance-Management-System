import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Index, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import ExcuseReason, ExcuseStatus
from app.models.mixins import Timestamps, UUIDPrimaryKey, fk
from app.models.user import User


class AbsenceExcuse(UUIDPrimaryKey, Timestamps, Base):
    """Student's request to excuse an absence (single approver: teacher or admin)."""

    __tablename__ = "absence_excuses"
    __table_args__ = (
        Index("ix_absence_excuses_student_id_status", "student_id", "status"),
        Index("ix_absence_excuses_start_date_end_date", "start_date", "end_date"),
    )

    student_id: Mapped[uuid.UUID] = fk("users.id")
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    reason: Mapped[ExcuseReason] = mapped_column(SAEnum(ExcuseReason, name="excuse_reason"))
    details: Mapped[str | None] = mapped_column(String(1000))
    attachment_url: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[ExcuseStatus] = mapped_column(
        SAEnum(ExcuseStatus, name="excuse_status"), default=ExcuseStatus.PENDING
    )

    reviewed_by_id: Mapped[uuid.UUID | None] = fk("users.id", ondelete="SET NULL")
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    review_comment: Mapped[str | None] = mapped_column(String(500))

    student: Mapped[User] = relationship(foreign_keys=[student_id])
    reviewed_by: Mapped[User | None] = relationship(foreign_keys=[reviewed_by_id])
