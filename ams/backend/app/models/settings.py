import datetime as dt

from sqlalchemy import CheckConstraint, Date, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import UUIDPrimaryKey


class SchoolSetting(Base):
    """Singleton row (id = 1) holding the attendance rules."""

    __tablename__ = "school_settings"
    __table_args__ = (CheckConstraint("id = 1", name="singleton"),)

    id: Mapped[int] = mapped_column(primary_key=True, default=1)
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Phnom_Penh")
    late_after_minutes: Mapped[int] = mapped_column(default=10)  # later than this => LATE
    absent_after_minutes: Mapped[int] = mapped_column(default=30)  # later than this => ABSENT
    low_attendance_percent: Mapped[int] = mapped_column(default=80)  # flag students below this


class SchoolLocation(UUIDPrimaryKey, Base):
    """Geofence centre + radius used for GPS check-in."""

    __tablename__ = "school_locations"

    name: Mapped[str] = mapped_column(String(100))
    latitude: Mapped[float]
    longitude: Mapped[float]
    radius_meters: Mapped[int] = mapped_column(default=150)
    is_active: Mapped[bool] = mapped_column(default=True)


class Holiday(UUIDPrimaryKey, Base):
    __tablename__ = "holidays"
    __table_args__ = (UniqueConstraint("date", "name"),)

    name: Mapped[str] = mapped_column(String(150))
    date: Mapped[dt.date] = mapped_column(Date)
    is_recurring: Mapped[bool] = mapped_column(default=False)
