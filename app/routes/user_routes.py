from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.dependencies.database_dependency import get_db
from app.schemas.user_schema import RoleEnum, UserCreate, UserPatch, UserResponse, UserUpdate
from app.services import user_service

router = APIRouter()


@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Retorna todos los usuarios. Permite filtrar por rol, estado activo y ordenar.",
)
def list_users(
    skip: int = Query(default=0, ge=0, description="Registros a omitir"),
    limit: int = Query(default=100, ge=1, le=500, description="Máximo de registros"),
    role: Optional[RoleEnum] = Query(default=None, description="Filtrar por rol"),
    is_active: Optional[bool] = Query(default=None, description="Filtrar por estado activo"),
    order_by: str = Query(default="id", pattern="^(id|name|created_at)$"),
    db: Session = Depends(get_db),
):
    return user_service.get_users(db, skip=skip, limit=limit, role=role, is_active=is_active, order_by=order_by)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
    responses={404: {"description": "Usuario no encontrado"}},
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuario con id={user_id} no encontrado.")
    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    responses={400: {"description": "Email duplicado"}, 422: {"description": "Datos inválidos"}},
)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario completo",
    responses={400: {"description": "Email duplicado"}, 404: {"description": "No encontrado"}},
)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    try:
        return user_service.update_user(db, user_id, data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario parcialmente",
    responses={400: {"description": "Email duplicado"}, 404: {"description": "No encontrado"}},
)
def patch_user(user_id: int, data: UserPatch, db: Session = Depends(get_db)):
    try:
        return user_service.patch_user(db, user_id, data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    responses={404: {"description": "No encontrado"}},
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user_service.delete_user(db, user_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
