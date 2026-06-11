from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"


class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, examples=["Ana Torres"])
    email: EmailStr = Field(..., examples=["ana@example.com"])
    role: RoleEnum = Field(..., examples=["user"])
    is_active: bool = Field(default=True)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío.")
        return v.strip()


class UserUpdate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    role: RoleEnum
    is_active: bool

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío.")
        return v.strip()


class UserPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=100)
    email: Optional[EmailStr] = Field(default=None)
    role: Optional[RoleEnum] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("El nombre no puede estar vacío.")
        return v.strip() if v else v


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
