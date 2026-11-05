"""Create the singleton settings row and the first admin account.

Run from the backend/ folder:  python -m scripts.seed
"""
from sqlalchemy import select

from app.core.config import settings
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models import SchoolSetting, User
from app.models.enums import Role


def main() -> None:
    with SessionLocal() as db:
        if db.get(SchoolSetting, 1) is None:
            db.add(SchoolSetting(id=1))
            print("Created default school settings")

        if db.scalar(select(User).where(User.email == settings.admin_email)) is None:
            db.add(
                User(
                    code="ADMIN-001",
                    email=settings.admin_email,
                    password_hash=hash_password(settings.admin_password),
                    first_name="System",
                    last_name="Admin",
                    role=Role.ADMIN,
                )
            )
            print(f"Created admin {settings.admin_email}")
        db.commit()


if __name__ == "__main__":
    main()
