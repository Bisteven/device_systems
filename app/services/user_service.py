from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserPatch, UserUpdate


def create_user(db: Session, data: UserCreate) -> User:
    if get_user_by_email(db, data.email):
        raise ValueError(f"El email '{data.email}' ya está registrado.")
    user = User(name=data.name, email=data.email, role=data.role, is_active=data.is_active)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    order_by: str = "id",
) -> List[User]:
    query = db.query(User)
    if role is not None:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    order_column = {"name": User.name, "created_at": User.created_at}.get(order_by, User.id)
    return query.order_by(order_column).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, user_id: int, data: UserUpdate) -> User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise LookupError(f"Usuario con id={user_id} no encontrado.")
    existing = get_user_by_email(db, data.email)
    if existing and existing.id != user_id:
        raise ValueError(f"El email '{data.email}' ya está en uso por otro usuario.")
    user.name = data.name
    user.email = data.email
    user.role = data.role
    user.is_active = data.is_active
    db.commit()
    db.refresh(user)
    return user


def patch_user(db: Session, user_id: int, data: UserPatch) -> User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise LookupError(f"Usuario con id={user_id} no encontrado.")
    updates = data.model_dump(exclude_unset=True)
    if "email" in updates:
        existing = get_user_by_email(db, updates["email"])
        if existing and existing.id != user_id:
            raise ValueError(f"El email '{updates['email']}' ya está en uso.")
    for field, value in updates.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> None:
    user = get_user_by_id(db, user_id)
    if not user:
        raise LookupError(f"Usuario con id={user_id} no encontrado.")
    db.delete(user)
    db.commit()
