from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, examples=["Ana Pérez"])
    email: EmailStr = Field(..., examples=["ana@sena.edu.co"])
    role: RoleEnum = Field(..., examples=["user"])
    is_active: bool = Field(default=True)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
