from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.dependencies.database_dependency import get_db
from app.schemas.device_schema import DeviceCreate, DevicePatch, DeviceResponse, DeviceTypeEnum, DeviceUpdate
from app.services import device_service

router = APIRouter()


@router.get(
    "/",
    response_model=List[DeviceResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar dispositivos",
    description="Retorna todos los dispositivos. Soporta filtros por tipo, disponibilidad, marca y búsqueda.",
)
def list_devices(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    device_type: Optional[DeviceTypeEnum] = Query(default=None, description="Filtrar por tipo de dispositivo"),
    is_available: Optional[bool] = Query(default=None, description="Filtrar por disponibilidad"),
    brand: Optional[str] = Query(default=None, description="Filtrar por marca"),
    search: Optional[str] = Query(default=None, description="Búsqueda por nombre, serial o marca"),
    db: Session = Depends(get_db),
):
    return device_service.get_devices(
        db, skip=skip, limit=limit,
        device_type=device_type, is_available=is_available,
        brand=brand, search=search,
    )


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener dispositivo por ID",
    responses={404: {"description": "Dispositivo no encontrado"}},
)
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = device_service.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail=f"Dispositivo con id={device_id} no encontrado.")
    return device


@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    responses={400: {"description": "Número de serie duplicado"}, 422: {"description": "Datos inválidos"}},
)
def create_device(data: DeviceCreate, db: Session = Depends(get_db)):
    try:
        return device_service.create_device(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar dispositivo completo",
    responses={400: {"description": "Serial duplicado"}, 404: {"description": "No encontrado"}},
)
def update_device(device_id: int, data: DeviceUpdate, db: Session = Depends(get_db)):
    try:
        return device_service.update_device(db, device_id, data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar dispositivo parcialmente",
    responses={400: {"description": "Serial duplicado"}, 404: {"description": "No encontrado"}},
)
def patch_device(device_id: int, data: DevicePatch, db: Session = Depends(get_db)):
    try:
        return device_service.patch_device(db, device_id, data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
    responses={404: {"description": "No encontrado"}},
)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    try:
        device_service.delete_device(db, device_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
