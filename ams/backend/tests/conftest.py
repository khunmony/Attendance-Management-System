import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401
from app.core.security import hash_password
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.enums import Role
from app.models.user import User


@pytest.fixture()
def db():
    """Fresh in-memory SQLite database per test (production uses PostgreSQL)."""
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, expire_on_commit=False)()
    yield session
    session.close()
    engine.dispose()


@pytest.fixture()
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def admin(db):
    user = User(
        code="ADMIN-001", email="admin@test.local", password_hash=hash_password("secret123"),
        first_name="Test", last_name="Admin", role=Role.ADMIN,
    )
    db.add(user)
    db.commit()
    return user
