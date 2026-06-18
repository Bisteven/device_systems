from typing import Generator
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency que provee una sesión de base de datos SQLAlchemy.
    Garantiza el cierre de la sesión al finalizar la solicitud.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
