"""
user_routes.py - Endpoints REST para el recurso /users.
Implementa GET (lista, por ID, filtros) y POST (registro).
"""

from fastapi import APIRouter, HTTPException, Query, Response, status
from app.schemas.user_schema import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Usuarios"])

# ---------------------------------------------------------------------------
# Base de datos en memoria (lista de diccionarios)
# ---------------------------------------------------------------------------
_db: list[dict] = [
    {"id": 1, "name": "Carlos Mendoza", "email": "carlos@devicesystems.com",  "role": "admin",   "is_active": True},
    {"id": 2, "name": "Laura Ríos",     "email": "laura@devicesystems.com",   "role": "support", "is_active": True},
    {"id": 3, "name": "Pedro Silva",    "email": "pedro@devicesystems.com",   "role": "user",    "is_active": False},
    {"id": 4, "name": "María Castro",   "email": "maria@devicesystems.com",   "role": "user",    "is_active": True},
]

_CUSTOM_HEADERS = {
    "X-App-Name": "device_systems",
    "X-API-Version": "1.0",
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

    resultado = list(_db)

    if role is not None:
        roles_validos = {"admin", "support", "user"}
        if role not in roles_validos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Rol inválido '{role}'. Los valores permitidos son: {sorted(roles_validos)}.",
            )
        resultado = [u for u in resultado if u["role"] == role]

    if is_active is not None:
        resultado = [u for u in resultado if u["is_active"] == is_active]

    return resultado


# ---------------------------------------------------------------------------
# GET /users/{user_id}
# ---------------------------------------------------------------------------
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Retorna un usuario específico usando su **ID** como path parameter.",
)
def get_user_by_id(user_id: int, response: Response) -> dict:
    _add_headers(response)

    usuario = next((u for u in _db if u["id"] == user_id), None)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un usuario con ID {user_id}.",
        )
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
)
def create_user(payload: UserCreate, response: Response) -> dict:
    _add_headers(response)

    # Verificar email duplicado
    if any(u["email"] == payload.email for u in _db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El correo '{payload.email}' ya está registrado.",
        )

    nuevo_id = max((u["id"] for u in _db), default=0) + 1
    nuevo_usuario = {
        "id": nuevo_id,
        "name": payload.name,
        "email": payload.email,
        "role": payload.role,
        "is_active": payload.is_active,
    }
    _db.append(nuevo_usuario)
    return nuevo_usuario
