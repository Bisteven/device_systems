# device_systems — API REST con FastAPI + SQLAlchemy

API REST para la gestión de usuarios del sistema **device_systems**.  
Esta versión reemplaza el almacenamiento en memoria por una base de datos relacional gestionada con **SQLAlchemy** y **SQLite**.

---

## Estructura del proyecto

```
device_systems/
├── app/
│   ├── main.py                          # Punto de entrada de la aplicación
│   ├── database/
│   │   └── connection.py                # Engine, SessionLocal y Base declarativa
│   ├── models/
│   │   └── user_model.py                # Modelo SQLAlchemy → tabla 'users'
│   ├── schemas/
│   │   └── user_schema.py               # Schemas Pydantic (entrada y salida)
│   ├── routes/
│   │   └── user_routes.py               # Endpoints REST del recurso /users
│   ├── services/
│   │   └── user_service.py              # Lógica de negocio y operaciones CRUD
│   └── dependencies/
│       └── database_dependency.py       # Dependencia get_db para FastAPI
├── requirements.txt
└── README.md
```

---

## Requisitos

- Python 3.10+
- pip

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd device_systems

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## Ejecución

```bash
uvicorn app.main:app --reload
```

La API quedará disponible en `http://127.0.0.1:8000`.

| Ruta | Descripción |
|------|-------------|
| `http://127.0.0.1:8000/docs` | Swagger UI |
| `http://127.0.0.1:8000/redoc` | ReDoc |

---

## Endpoints disponibles

| Método | Ruta | Descripción | Código éxito |
|--------|------|-------------|:---:|
| `GET` | `/users` | Listar usuarios (con filtros) | 200 |
| `GET` | `/users/{user_id}` | Obtener usuario por ID | 200 |
| `POST` | `/users` | Crear usuario | 201 |
| `PUT` | `/users/{user_id}` | Actualizar usuario completo | 200 |
| `PATCH` | `/users/{user_id}` | Actualizar usuario parcialmente | 200 |
| `DELETE` | `/users/{user_id}` | Eliminar usuario | 204 |

### Parámetros de filtrado en GET /users

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `skip` | int | Registros a saltar (paginación) |
| `limit` | int | Máximo de registros (1–500) |
| `role` | string | Filtrar por rol: `admin`, `support`, `user` |
| `is_active` | bool | Filtrar por estado activo |
| `order_by` | string | Ordenar por: `id`, `name`, `created_at` |

---

## Modelo SQLAlchemy vs Schema Pydantic

| Aspecto | Modelo SQLAlchemy (`user_model.py`) | Schema Pydantic (`user_schema.py`) |
|---------|-------------------------------------|------------------------------------|
| **Propósito** | Representar la tabla en la base de datos | Validar y serializar datos de la API |
| **Ubicación** | Capa de persistencia | Capa de presentación / entrada |
| **Hereda de** | `Base` (declarative_base) | `BaseModel` |
| **Ejemplo** | `Column(String, nullable=False)` | `Field(..., min_length=3)` |
| **Visibilidad** | Interna (ORM ↔ BD) | Externa (HTTP request/response) |

---

## Códigos de error

| Caso | Código |
|------|:------:|
| Usuario creado | 201 Created |
| Consulta / actualización exitosa | 200 OK |
| Eliminación exitosa | 204 No Content |
| Usuario no encontrado | 404 Not Found |
| Email duplicado | 400 Bad Request |
| Rol no permitido / datos inválidos | 422 Unprocessable Entity |

---

## Validaciones aplicadas

- **name**: obligatorio, mínimo 3 caracteres, sin espacios en blanco al inicio/fin.
- **email**: formato de email válido, único en la base de datos.
- **role**: solo acepta `admin`, `support` o `user` (Enum).
- **is_active**: booleano con valor por defecto `true`.

---

## Rama de desarrollo

Este proyecto usa la rama `feature/sqlalchemy-persistence` para la integración de SQLAlchemy.

```bash
git checkout feature/sqlalchemy-persistence
```

---

## Reflexión final

Incorporar persistencia real con SQLAlchemy transforma la API de un prototipo en memoria a una aplicación lista para producción. El ORM desacopla el código Python de los detalles del motor de base de datos, facilitando futuros cambios (p. ej., migrar de SQLite a PostgreSQL modificando solo la `DATABASE_URL`). Los schemas Pydantic, por su parte, protegen la API de datos malformados antes de que lleguen a la capa de persistencia, separando claramente responsabilidades.
