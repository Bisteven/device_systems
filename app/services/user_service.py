"""
user_service.py - Lógica de negocio para el recurso usuarios.
Centraliza operaciones CRUD sobre la base de datos en memoria.
"""

from fastapi import HTTPException, status
from app.data.users_db import users_db
from app.schemas.user_schema import UserCreate, UserUpdate


ROLES_VALIDOS = {"admin", "support", "user"}


def get_all_users(role: str | None, is_active: bool | None) -> list[dict]:
    """Retorna todos los usuarios, con filtros opcionales por rol y estado."""
    if role is not None and role not in ROLES_VALIDOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": True,
                "message": f"Rol inválido '{role}'. Los valores permitidos son: {sorted(ROLES_VALIDOS)}.",
                "status_code": 400,
            },
        )
    resultado = list(users_db)
    if role is not None:
        resultado = [u for u in resultado if u["role"] == role]
    if is_active is not None:
        resultado = [u for u in resultado if u["is_active"] == is_active]
    return resultado


def get_user_by_id_or_404(user_id: int) -> dict:
    """Busca un usuario por ID. Lanza 404 si no existe."""
    usuario = next((u for u in users_db if u["id"] == user_id), None)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": True,
                "message": f"No existe un usuario con ID {user_id}.",
                "status_code": 404,
            },
        )
    return usuario


def create_user(payload: UserCreate) -> dict:
    """Crea un nuevo usuario. Valida duplicidad de correo."""
    if any(u["email"] == payload.email for u in users_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": True,
                "message": f"El correo '{payload.email}' ya está registrado.",
                "status_code": 400,
            },
        )
    nuevo_id = max((u["id"] for u in users_db), default=0) + 1
    nuevo_usuario = {
        "id": nuevo_id,
        "name": payload.name,
        "email": payload.email,
        "role": payload.role,
        "is_active": payload.is_active,
    }
    users_db.append(nuevo_usuario)
    return nuevo_usuario


def update_user_full(user_id: int, payload: UserCreate) -> dict:
    """Reemplaza completamente un usuario existente (PUT)."""
    usuario = get_user_by_id_or_404(user_id)

    # Verificar que el nuevo email no pertenezca a otro usuario
    email_conflict = next(
        (u for u in users_db if u["email"] == payload.email and u["id"] != user_id),
        None,
    )
    if email_conflict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": True,
                "message": f"El correo '{payload.email}' ya está en uso por otro usuario.",
                "status_code": 400,
            },
        )

    usuario.update({
        "name": payload.name,
        "email": payload.email,
        "role": payload.role,
        "is_active": payload.is_active,
    })
    return usuario


def update_user_partial(user_id: int, payload: UserUpdate) -> dict:
    """Actualiza solo los campos enviados de un usuario (PATCH)."""
    usuario = get_user_by_id_or_404(user_id)

    campos = payload.model_dump(exclude_unset=True)
    if not campos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": True,
                "message": "Debes enviar al menos un campo para actualizar.",
                "status_code": 400,
            },
        )

    # Verificar conflicto de email
    if "email" in campos:
        email_conflict = next(
            (u for u in users_db if u["email"] == campos["email"] and u["id"] != user_id),
            None,
        )
        if email_conflict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": True,
                    "message": f"El correo '{campos['email']}' ya está en uso por otro usuario.",
                    "status_code": 400,
                },
            )

    usuario.update(campos)
    return usuario


def delete_user(user_id: int) -> None:
    """Elimina un usuario por ID. Lanza 404 si no existe."""
    usuario = get_user_by_id_or_404(user_id)
    users_db.remove(usuario)
