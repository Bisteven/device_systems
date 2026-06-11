from fastapi import FastAPI
from app.database.connection import Base, engine
from app.routes.user_routes import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Device Systems API",
    description="API REST para la gestión de usuarios del sistema device_systems con persistencia SQLAlchemy.",
    version="2.0.0",
    contact={
        "name": "Device Systems",
        "email": "admin@devicesystems.com",
    },
)

app.include_router(user_router, prefix="/users", tags=["Users"])


@app.get("/", tags=["Root"])
def root():
    return {"message": "Device Systems API v2.0 - SQLAlchemy Edition", "docs": "/docs"}
