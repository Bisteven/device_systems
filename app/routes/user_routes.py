"""
user_routes.py - Endpoints REST para el recurso /users.
Implementa CRUD completo: GET, POST, PUT, PATCH, DELETE.
Utiliza servicios y dependencias reutilizables con Depends().
"""

from fastapi import APIRouter, Depends, Query, Response, status
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.services import user_service
from app.dependencies.user_dependencies import get_user_or_404, get_api_config

router = APIRouter(prefix="/users", tags=["Usuarios"])

_CUSTOM_HEADERS = {
    "X-App-Name": "device_systems",
    "X-API-Version": "2.0",
}


def _add_headers(response: Response) -> None:
    """Agrega las cabeceras personalizadas a la respuesta HTTP."""
    for key, value in _CUSTOM_HEADERS.items():
        response.headers[key] = value


# ---------------------------------------------------------------------------
# GET /users
# ---------------------------------------------------------------------------
@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description=(
        "Retorna todos los usuarios registrados. "
        "Permite filtrar por **rol** y/o **estado activo** usando query parameters."
    ),
    response_description="Lista de usuarios que cumplen los filtros aplicados.",
)
def get_users(
    response: Response,
    role: str | None = Query(
        None,
        description="Filtra por rol: admin, support o user.",
        examples=["admin"],
    ),
    is_active: bool | None = Query(
        None,
        description="Filtra por estado: true = activos, false = inactivos.",
    ),
) -> list[dict]:
    _add_headers(response)
    return user_service.get_all_users(role, is_active)


# ---------------------------------------------------------------------------
# GET /users/{user_id}
# ---------------------------------------------------------------------------
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Retorna un usuario específico usando su **ID** como path parameter.",
    response_description="Datos completos del usuario encontrado.",
)
def get_user_by_id(
    response: Response,
    usuario: dict = Depends(get_user_or_404),
) -> dict:
    _add_headers(response)
    return usuario


# ---------------------------------------------------------------------------
# POST /users
# ---------------------------------------------------------------------------
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    description=(
        "Registra un nuevo usuario en el sistema. "
        "Valida los datos con Pydantic y rechaza correos duplicados."
    ),
    response_description="Datos del usuario recién creado.",
)
def create_user(payload: UserCreate, response: Response) -> dict:
    _add_headers(response)
    return user_service.create_user(payload)


# ---------------------------------------------------------------------------
# PUT /users/{user_id}
# ---------------------------------------------------------------------------
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo (PUT)",
    description=(
        "Reemplaza **todos** los campos del usuario con el ID indicado. "
        "Requiere enviar name, email, role e is_active."
    ),
    response_description="Datos actualizados del usuario.",
)
def update_user_full(
    payload: UserCreate,
    response: Response,
    usuario: dict = Depends(get_user_or_404),
) -> dict:
    _add_headers(response)
    return user_service.update_user_full(usuario["id"], payload)


# ---------------------------------------------------------------------------
# PATCH /users/{user_id}
# ---------------------------------------------------------------------------
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcialmente (PATCH)",
    description=(
        "Modifica **solo los campos enviados** del usuario con el ID indicado. "
        "Si no se envía ningún campo, responde con 400 Bad Request."
    ),
    response_description="Datos actualizados del usuario tras el parche.",
)
def update_user_partial(
    payload: UserUpdate,
    response: Response,
    usuario: dict = Depends(get_user_or_404),
) -> dict:
    _add_headers(response)
    return user_service.update_user_partial(usuario["id"], payload)


# ---------------------------------------------------------------------------
# DELETE /users/{user_id}
# ---------------------------------------------------------------------------
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar usuario",
    description="Elimina el usuario con el ID indicado. Responde 404 si no existe.",
    response_description="Mensaje de confirmación de eliminación.",
)
def delete_user(
    response: Response,
    usuario: dict = Depends(get_user_or_404),
) -> dict:
    _add_headers(response)
    user_service.delete_user(usuario["id"])
    return {
        "error": False,
        "message": f"Usuario con ID {usuario['id']} eliminado correctamente.",
        "status_code": 200,
    }
