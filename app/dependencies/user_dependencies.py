"""
user_dependencies.py - Dependencias reutilizables con Depends() para el recurso usuarios.
Centraliza la validación de IDs, correos y roles para ser inyectada en los endpoints.
"""

from fastapi import Depends, Header, HTTPException, Path, status
from app.data.users_db import users_db
from app.schemas.user_schema import ROLES_VALIDOS  # type: ignore[attr-defined]

# Roles permitidos (se redefinen aquí para poder importarlas directamente)
_ROLES_VALIDOS = {"admin", "support", "user"}

# Cabecera de autenticación simulada
_API_TOKEN_VALIDO = "device-token-2025"


def get_user_or_404(
    user_id: int = Path(..., description="ID del usuario a consultar.", ge=1),
) -> dict:
    """
    Dependencia que busca un usuario por ID en la base de datos.
    Lanza HTTPException 404 si no existe.
    Úsala con Depends() en cualquier endpoint que necesite un usuario específico.
    """
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


def validate_role_param(role: str) -> str:
    """
    Valida que el parámetro de rol sea uno de los valores permitidos.
    Úsala con Depends() en endpoints con filtro por rol.
    """
    if role not in _ROLES_VALIDOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": True,
                "message": f"Rol inválido '{role}'. Los permitidos son: {sorted(_ROLES_VALIDOS)}.",
                "status_code": 400,
            },
        )
    return role


def verify_email_not_duplicated(email: str, exclude_id: int | None = None) -> str:
    """
    Verifica que un correo no esté ya registrado en la base de datos.
    Opcionalmente excluye a un usuario por ID (útil en PUT/PATCH).
    """
    conflict = next(
        (u for u in users_db if u["email"] == email and u["id"] != exclude_id),
        None,
    )
    if conflict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": True,
                "message": f"El correo '{email}' ya está en uso.",
                "status_code": 400,
            },
        )
    return email


def get_api_config() -> dict:
    """
    Dependencia que retorna la configuración general de la API.
    Puede usarse para exponer metadatos en cualquier endpoint.
    """
    return {
        "app": "device_systems",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


def simulate_auth(x_api_token: str | None = Header(default=None)) -> str:
    """
    Simula autenticación básica mediante la cabecera X-API-Token.
    Si la cabecera no está presente o es incorrecta, devuelve 401.

    Para probar en Swagger: envía la cabecera X-Api-Token: device-token-2025
    """
    if x_api_token != _API_TOKEN_VALIDO:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": True,
                "message": "Token de autenticación inválido o ausente.",
                "status_code": 401,
            },
        )
    return x_api_token
