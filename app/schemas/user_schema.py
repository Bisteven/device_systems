"""
user_schema.py - Modelos Pydantic v2 para el recurso usuarios.
Define los esquemas de entrada (UserCreate, UserUpdate) y salida (UserResponse).
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from enum import Enum


class Role(str, Enum):
    """Roles permitidos dentro del sistema device_systems."""
    admin = "admin"
    support = "support"
    user = "user"


class UserCreate(BaseModel):
    """Esquema de entrada para registrar un nuevo usuario."""

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nombre completo del usuario (mínimo 3 caracteres).",
        examples=["Ana García"],
    )
    email: EmailStr = Field(
        ...,
        description="Correo electrónico válido y único.",
        examples=["ana.garcia@devicesystems.com"],
    )
    role: Role = Field(
        ...,
        description="Rol del usuario: admin, support o user.",
        examples=["user"],
    )
    is_active: bool = Field(
        True,
        description="Indica si el usuario está activo en el sistema.",
    )

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío o ser solo espacios.")
        return v.strip().title()


class UserUpdate(BaseModel):
    """Esquema de entrada para actualización parcial (PATCH) de un usuario.
    Todos los campos son opcionales — solo se actualizan los campos enviados.
    """

    name: str | None = Field(
        None,
        min_length=3,
        max_length=100,
        description="Nuevo nombre completo.",
        examples=["Ana García"],
    )
    email: EmailStr | None = Field(
        None,
        description="Nuevo correo electrónico.",
        examples=["nuevo@devicesystems.com"],
    )
    role: Role | None = Field(
        None,
        description="Nuevo rol: admin, support o user.",
        examples=["support"],
    )
    is_active: bool | None = Field(
        None,
        description="Nuevo estado activo/inactivo.",
    )

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("El nombre no puede estar vacío o ser solo espacios.")
        return v.strip().title() if v else v


class UserResponse(BaseModel):
    """Esquema de salida — solo expone los campos necesarios al cliente."""

    id: int = Field(..., description="Identificador único del usuario.")
    name: str
    email: EmailStr
    role: Role
    is_active: bool

    model_config = {"from_attributes": True}
