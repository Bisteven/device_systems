"""
user_schema.py - Modelos Pydantic v2 para el recurso usuarios.
Define los esquemas de entrada (UserCreate) y salida (UserResponse).
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


class UserResponse(BaseModel):
    """Esquema de salida — solo expone los campos necesarios al cliente."""

    id: int = Field(..., description="Identificador único del usuario.")
    name: str
    email: EmailStr
    role: Role
    is_active: bool

    model_config = {"from_attributes": True}
