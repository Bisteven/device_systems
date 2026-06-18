from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    serial_number = Column(String(100), unique=True, nullable=False, index=True)
    device_type = Column(String(50), nullable=False)
    brand = Column(String(100), nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    loans = relationship("Loan", back_populates="device")
