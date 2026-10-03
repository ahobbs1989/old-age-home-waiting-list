"""Database engine and session helper."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlmodel import Session, SQLModel, create_engine

from app.config import DB_PATH

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    """Create all tables that don't already exist."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Iterator[Session]:
    """Yield a short-lived session for a single operation.

    `expire_on_commit=False` so model attributes stay readable after the
    `with` block closes the session (NiceGUI pages read them while building
    the UI, which commonly happens after the crud call that committed them).
    """
    with Session(engine, expire_on_commit=False) as session:
        yield session
