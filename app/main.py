"""
main.py - Punto de entrada de la API device_systems.
Inicializa FastAPI, registra los routers y configura metadatos de la documentación.
"""

from fastapi import FastAPI
from app.routes.user_routes import router as user_router

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios del sistema **device_systems**. "
        "Permite registrar, consultar y filtrar usuarios con validación de datos mediante Pydantic v2."
    ),
    version="1.0.0",
    contact={
        "name": "device_systems Team",
        "email": "soporte@devicesystems.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Registrar rutas
app.include_router(user_router)


@app.get("/", tags=["Root"], summary="Estado del servicio")
def root() -> dict:
    """Endpoint de bienvenida — verifica que el servidor esté en línea."""
    return {
        "app": "device_systems",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs",
    }
