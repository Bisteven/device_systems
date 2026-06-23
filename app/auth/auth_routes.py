from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.auth import auth_service
from app.limiter import limiter
from app.dependencies.auth_dependency import get_current_active_user
from app.dependencies.database_dependency import get_db
from app.models.user_model import User
from app.schemas.auth_schema import AuthUserResponse, Token, UserLogin, UserRegister

router = APIRouter()


@router.post(
    "/register",
    response_model=AuthUserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    responses={
        400: {"description": "Email duplicado"},
        422: {"description": "Contraseña débil o datos inválidos"},
        429: {"description": "Demasiadas solicitudes"},
    },
)
@limiter.limit("3/minute")
def register(request: Request, data: UserRegister, db: Session = Depends(get_db)):
    try:
        return auth_service.register_user(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    responses={
        401: {"description": "Credenciales incorrectas"},
        429: {"description": "Demasiadas solicitudes"},
    },
)
@limiter.limit("5/minute")
def login(request: Request, data: UserLogin, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_user_token(user)
    return Token(access_token=access_token, token_type="bearer")


@router.get(
    "/me",
    response_model=AuthUserResponse,
    summary="Perfil del usuario autenticado",
    responses={401: {"description": "Token inválido o no proporcionado"}},
)
def read_me(current_user: User = Depends(get_current_active_user)):
    return current_user
