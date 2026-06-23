import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.schemas.user_schema import RoleEnum


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, examples=["Ana Pérez"])
    email: EmailStr = Field(..., examples=["ana@sena.edu.co"])
    password: str = Field(..., min_length=8, max_length=128)
    role: RoleEnum = Field(default=RoleEnum.user, examples=["user"])

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if " " in value or "\t" in value:
            raise ValueError("La contraseña no puede contener espacios en blanco.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe incluir al menos una letra mayúscula.")
        if not re.search(r"[a-z]", value):
            raise ValueError("La contraseña debe incluir al menos una letra minúscula.")
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe incluir al menos un número.")
        return value


class UserLogin(BaseModel):
    email: EmailStr = Field(..., examples=["ana@sena.edu.co"])
    password: str = Field(..., min_length=1, examples=["MiClave123"])


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None


class AuthUserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
