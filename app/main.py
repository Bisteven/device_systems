from fastapi import FastAPI
from app.database.connection import Base, engine
from app.models import user_model, device_model, loan_model  # noqa: F401 – importar para que Alembic detecte los modelos
from app.routes import user_routes, device_routes, loan_routes

# Crear tablas automáticamente si no existen (útil en desarrollo sin Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para gestión de usuarios, dispositivos y préstamos. "
        "Construida con FastAPI + SQLAlchemy + Alembic."
    ),
    version="3.0.0",
    contact={"name": "Estiven", "email": "estiven@devicesystems.com"},
)

app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(device_routes.router, prefix="/devices", tags=["Devices"])
app.include_router(loan_routes.router, prefix="/loans", tags=["Loans"])


@app.get("/", tags=["Health"])
def root():
    return {"message": "device_systems API v3.0 — /docs para la documentación"}
