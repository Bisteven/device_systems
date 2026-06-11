from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from enum import Enum

app = FastAPI(
    title="Device Systems API",
    description="API REST para la gestión de usuarios del sistema device_systems (almacenamiento en memoria).",
    version="1.0.0",
)

# ── In-memory store ───────────────────────────────────────────────────────────
_users: List[dict] = []
_next_id: int = 1


class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"


class UserIn(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: RoleEnum
    is_active: bool = True


class UserOut(UserIn):
    id: int


@app.get("/users", response_model=List[UserOut])
def list_users():
    return _users


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    user = next((u for u in _users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return user


@app.post("/users", response_model=UserOut, status_code=201)
def create_user(data: UserIn):
    global _next_id
    if any(u["email"] == data.email for u in _users):
        raise HTTPException(status_code=400, detail="Email ya registrado.")
    user = {"id": _next_id, **data.model_dump()}
    _next_id += 1
    _users.append(user)
    return user


@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, data: UserIn):
    user = next((u for u in _users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    user.update(data.model_dump())
    return user


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    global _users
    user = next((u for u in _users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    _users = [u for u in _users if u["id"] != user_id]
