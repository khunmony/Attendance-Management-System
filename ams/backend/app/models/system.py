import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Index, String, Text, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import NotificationType
from app.models.mixins import UUIDPrimaryKey, fk

# JSONB on PostgreSQL, plain JSON elsewhere (e.g. SQLite in tests)
JSONType = JSON().with_variant(JSONB(), "postgresql")


class Notification(UUIDPrimaryKey, Base):
    __tablename__ = "notifications"
    __table_args__ = (Index("ix_notifications_user_id_read_at", "user_id", "read_at"),)

    user_id: Mapped[uuid.UUID] = fk("users.id")
    type: Mapped[NotificationType] = mapped_column(
        SAEnum(NotificationType, name="notification_type")
    )
    title: Mapped[str] = mapped_column(String(200))
    body: Mapped[str] = mapped_column(Text)
    link: Mapped[str | None] = mapped_column(String(300))
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class AuditLog(UUIDPrimaryKey, Base):
    __tablename__ = "audit_logs"
    __table_args__ = (Index("ix_audit_logs_entity_type_entity_id", "entity_type", "entity_id"),)

    actor_id: Mapped[uuid.UUID | None] = fk("users.id", ondelete="SET NULL", index=True)
    action: Mapped[str] = mapped_column(String(100))  # e.g. "ATTENDANCE_OVERRIDE"
    entity_type: Mapped[str] = mapped_column(String(100))
    entity_id: Mapped[str] = mapped_column(String(64))
    before: Mapped[dict | None] = mapped_column(JSONType)
    after: Mapped[dict | None] = mapped_column(JSONType)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
