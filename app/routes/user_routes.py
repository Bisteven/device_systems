from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.user_schema import RoleEnum, UserCreate, UserPatch, UserResponse, UserUpdate
from app.services import user_service

router = APIRouter()


# ── GET /users ─────────────────────────────────────────────────────────────────

@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description=(
        "Retorna todos los usuarios. Permite filtrar por **rol** o **estado activo**, "
        "y ordenar por `id`, `name` o `created_at`."
    ),
)
def list_users(
    skip: int = Query(default=0, ge=0, description="Registros a omitir (paginación)"),
    limit: int = Query(default=100, ge=1, le=500, description="Máximo de registros a retornar"),
    role: Optional[RoleEnum] = Query(default=None, description="Filtrar por rol"),
    is_active: Optional[bool] = Query(default=None, description="Filtrar por estado activo"),
    order_by: str = Query(
        default="id",
        pattern="^(id|name|created_at)$",
        description="Campo por el que ordenar",
    ),
    db: Session = Depends(get_db),
):
    return user_service.get_users(
        db, skip=skip, limit=limit, role=role, is_active=is_active, order_by=order_by
    )


# ── GET /users/{user_id} ───────────────────────────────────────────────────────

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
    description="Retorna un único usuario identificado por su **id**.",
    responses={404: {"description": "Usuario no encontrado"}},
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id={user_id} no encontrado.",
        )
    return user


# ── POST /users ────────────────────────────────────────────────────────────────

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Crea un nuevo usuario en la base de datos.",
    responses={
        400: {"description": "Email duplicado"},
        422: {"description": "Datos de entrada inválidos"},
    },
)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


# ── PUT /users/{user_id} ───────────────────────────────────────────────────────

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario completo",
    description="Reemplaza **todos** los campos editables de un usuario (PUT completo).",
    responses={
        400: {"description": "Email duplicado"},
        404: {"description": "Usuario no encontrado"},
        422: {"description": "Datos de entrada inválidos"},
    },
)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    try:
        return user_service.update_user(db, user_id, data)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


# ── PATCH /users/{user_id} ─────────────────────────────────────────────────────

@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario parcialmente",
    description="Actualiza **solo los campos enviados** en el cuerpo de la petición (PATCH parcial).",
    responses={
        400: {"description": "Email duplicado"},
        404: {"description": "Usuario no encontrado"},
        422: {"description": "Datos de entrada inválidos"},
    },
)
def patch_user(user_id: int, data: UserPatch, db: Session = Depends(get_db)):
    try:
        return user_service.patch_user(db, user_id, data)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


# ── DELETE /users/{user_id} ────────────────────────────────────────────────────

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina permanentemente un usuario de la base de datos.",
    responses={404: {"description": "Usuario no encontrado"}},
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user_service.delete_user(db, user_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
