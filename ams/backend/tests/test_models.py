from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable

from app.db.base import Base
import app.models  # noqa: F401


def test_all_tables_compile_for_postgresql():
    """The DDL must be valid for PostgreSQL even though tests run on SQLite."""
    for table in Base.metadata.sorted_tables:
        CreateTable(table).compile(dialect=postgresql.dialect())
