import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import Role
from app.models.mixins import Timestamps, UUIDPrimaryKey, fk


class User(UUIDPrimaryKey, Timestamps, Base):
    __tablename__ = "users"

    code: Mapped[str] = mapped_column(String(50), unique=True)  # student ID or staff ID
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    role: Mapped[Role] = mapped_column(SAEnum(Role, name="role"), index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    phone: Mapped[str | None] = mapped_column(String(30))

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class RefreshToken(UUIDPrimaryKey, Base):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[uuid.UUID] = fk("users.id", index=True)
    token_hash: Mapped[str] = mapped_column(String(255), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
