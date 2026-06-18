from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.dependencies.database_dependency import get_db
from app.schemas.loan_schema import LoanCreate, LoanDetailResponse, LoanResponse, LoanStatusEnum
from app.services import loan_service

router = APIRouter()


@router.get(
    "/details",
    response_model=List[LoanDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar préstamos con detalle de usuario y dispositivo",
    description="Retorna préstamos con join de usuario y dispositivo. Soporta filtros por estado, email y tipo.",
)
def list_loans_detail(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    status: Optional[LoanStatusEnum] = Query(default=None, description="Filtrar por estado"),
    user_email: Optional[str] = Query(default=None, description="Filtrar por email del usuario"),
    device_type: Optional[str] = Query(default=None, description="Filtrar por tipo de dispositivo"),
    db: Session = Depends(get_db),
):
    return loan_service.get_loans_detail(
        db, skip=skip, limit=limit,
        status=status, user_email=user_email, device_type=device_type,
    )


@router.get(
    "/",
    response_model=List[LoanResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar préstamos",
    description="Retorna préstamos con filtros opcionales por estado, usuario, dispositivo, email y tipo.",
)
def list_loans(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    status: Optional[LoanStatusEnum] = Query(default=None),
    user_id: Optional[int] = Query(default=None),
    device_id: Optional[int] = Query(default=None),
    user_email: Optional[str] = Query(default=None),
    device_type: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    return loan_service.get_loans(
        db, skip=skip, limit=limit,
        status=status, user_id=user_id, device_id=device_id,
        user_email=user_email, device_type=device_type,
    )


@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener préstamo por ID",
    responses={404: {"description": "Préstamo no encontrado"}},
)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = loan_service.get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail=f"Préstamo con id={loan_id} no encontrado.")
    return loan


@router.post(
    "/",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo",
    description="Crea un préstamo validando que el usuario y el dispositivo existan y que el dispositivo esté disponible.",
    responses={
        404: {"description": "Usuario o dispositivo no encontrado"},
        409: {"description": "Dispositivo no disponible"},
        422: {"description": "Datos inválidos"},
    },
)
def create_loan(data: LoanCreate, db: Session = Depends(get_db)):
    try:
        return loan_service.create_loan(db, data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    status_code=status.HTTP_200_OK,
    summary="Devolver dispositivo",
    description="Marca el préstamo como devuelto, registra la fecha de devolución y libera el dispositivo.",
    responses={
        404: {"description": "Préstamo no encontrado"},
        409: {"description": "El préstamo ya fue devuelto"},
    },
)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    try:
        return loan_service.return_loan(db, loan_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


# ── Rutas de consulta con joins por recurso ────────────────────────────────────

@router.get(
    "/user/{user_id}",
    response_model=List[LoanResponse],
    status_code=status.HTTP_200_OK,
    summary="Préstamos de un usuario",
    description="Retorna el historial completo de préstamos de un usuario específico.",
    responses={404: {"description": "Usuario no encontrado"}},
)
def loans_by_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return loan_service.get_loans_by_user(db, user_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get(
    "/device/{device_id}",
    response_model=List[LoanResponse],
    status_code=status.HTTP_200_OK,
    summary="Historial de préstamos de un dispositivo",
    description="Retorna todos los préstamos históricos de un dispositivo específico.",
    responses={404: {"description": "Dispositivo no encontrado"}},
)
def loans_by_device(device_id: int, db: Session = Depends(get_db)):
    try:
        return loan_service.get_loans_by_device(db, device_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
