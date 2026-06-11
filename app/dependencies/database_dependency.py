from typing import Generator

from sqlalchemy.orm import Session

from app.database.connection import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a SQLAlchemy database session.

    Yields a session and guarantees it is closed after the request
    completes, whether it succeeded or raised an exception.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
