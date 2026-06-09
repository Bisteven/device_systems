"""
users_db.py - Simulación de base de datos en memoria para el recurso usuarios.
"""

users_db: list[dict] = [
    {"id": 1, "name": "Carlos Mendoza", "email": "carlos@devicesystems.com",  "role": "admin",   "is_active": True},
    {"id": 2, "name": "Laura Ríos",     "email": "laura@devicesystems.com",   "role": "support", "is_active": True},
    {"id": 3, "name": "Pedro Silva",    "email": "pedro@devicesystems.com",   "role": "user",    "is_active": False},
    {"id": 4, "name": "María Castro",   "email": "maria@devicesystems.com",   "role": "user",    "is_active": True},
]
