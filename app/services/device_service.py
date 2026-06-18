from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DevicePatch, DeviceUpdate


def create_device(db: Session, data: DeviceCreate) -> Device:
    if db.query(Device).filter(Device.serial_number == data.serial_number).first():
        raise ValueError(f"El serial '{data.serial_number}' ya está registrado.")
    device = Device(
        name=data.name,
        serial_number=data.serial_number,
        device_type=data.device_type,
        brand=data.brand,
        is_available=data.is_available,
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def get_devices(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
) -> List[Device]:
    query = db.query(Device)
    if device_type:
        query = query.filter(Device.device_type == device_type)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search:
        query = query.filter(
            or_(
                Device.name.ilike(f"%{search}%"),
                Device.serial_number.ilike(f"%{search}%"),
                Device.brand.ilike(f"%{search}%"),
            )
        )
    return query.offset(skip).limit(limit).all()


def get_device_by_id(db: Session, device_id: int) -> Optional[Device]:
    return db.query(Device).filter(Device.id == device_id).first()


def update_device(db: Session, device_id: int, data: DeviceUpdate) -> Device:
    device = get_device_by_id(db, device_id)
    if not device:
        raise LookupError(f"Dispositivo con id={device_id} no encontrado.")
    existing = db.query(Device).filter(Device.serial_number == data.serial_number).first()
    if existing and existing.id != device_id:
        raise ValueError(f"El serial '{data.serial_number}' ya está registrado en otro dispositivo.")
    device.name = data.name
    device.serial_number = data.serial_number
    device.device_type = data.device_type
    device.brand = data.brand
    device.is_available = data.is_available
    db.commit()
    db.refresh(device)
    return device


def patch_device(db: Session, device_id: int, data: DevicePatch) -> Device:
    device = get_device_by_id(db, device_id)
    if not device:
        raise LookupError(f"Dispositivo con id={device_id} no encontrado.")
    updates = data.model_dump(exclude_unset=True)
    if "serial_number" in updates:
        existing = db.query(Device).filter(Device.serial_number == updates["serial_number"]).first()
        if existing and existing.id != device_id:
            raise ValueError(f"El serial '{updates['serial_number']}' ya está registrado en otro dispositivo.")
    for field, value in updates.items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device_id: int) -> None:
    device = get_device_by_id(db, device_id)
    if not device:
        raise LookupError(f"Dispositivo con id={device_id} no encontrado.")
    db.delete(device)
    db.commit()
