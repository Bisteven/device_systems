import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.auth import auth_routes
from app.database.connection import Base, engine
from app.limiter import limiter
from app.middlewares.request_middleware import RequestMiddleware
from app.models import user_model, device_model, loan_model  # noqa: F401
from app.routes import user_routes, device_routes, loan_routes

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST segura para gestión de usuarios, dispositivos y préstamos. "
        "Incluye autenticación OAuth2 con JWT, rate limiting, CORS y middleware de seguridad."
    ),
    version="3.0.0",
    contact={"name": "Estiven", "email": "estiven@devicesystems.com"},
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestMiddleware)

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(device_routes.router, prefix="/devices", tags=["Devices"])
app.include_router(loan_routes.router, prefix="/loans", tags=["Loans"])


@app.get("/", tags=["Security"])
def root():
    return {
        "message": "device_systems API v3.0 — /docs para la documentación",
        "security": "OAuth2 Bearer JWT — usar /auth/login para obtener token",
    }
