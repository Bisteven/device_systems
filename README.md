# device_systems API

API REST construida con **FastAPI** para la gestión de usuarios del sistema `device_systems`.  
Aplica validación de datos con **Pydantic v2**, response models, path/query parameters y cabeceras HTTP personalizadas.

---

## Estructura del proyecto
device_systems/
├── app/
│   ├── main.py                 # Punto de entrada, instancia FastAPI
│   ├── schemas/
│   │   └── user_schema.py      # Modelos Pydantic (UserCreate, UserResponse)
│   └── routes/
│       └── user_routes.py      # Endpoints GET y POST de /users
├── requirements.txt
├── .gitignore
└── README.md
|
└── capturas/




---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Bisteven/device_systems.git
cd device_systems

# 2. Crear y activar el entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1     # Windows PowerShell
source venv/bin/activate        # macOS/Linux

# 3. Instalar dependencias
python -m pip install fastapi uvicorn "pydantic[email]" --only-binary=:all:
```


![Instalación de dependencias](capturas/01_instalacion.png)

---

## Ejecución

```bash
python -m uvicorn app.main:app --reload
```

La API estará disponible en: `http://127.0.0.1:8000`  
Documentación interactiva: `http://127.0.0.1:8000/docs`

![Servidor corriendo](capturas/02_servidor.png)

---

## Swagger UI

Interfaz interactiva generada automáticamente por FastAPI en `/docs`.


![Swagger UI](capturas/03_swagger_general.png)

---

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Estado del servicio |
| GET | `/users/` | Listar todos los usuarios |
| GET | `/users/{user_id}` | Obtener usuario por ID |
| GET | `/users/?role=admin` | Filtrar por rol |
| GET | `/users/?is_active=true` | Filtrar por estado |
| POST | `/users/` | Registrar nuevo usuario |

---

## Pruebas de endpoints

### GET /users/ — Listar todos los usuarios

```http
GET http://127.0.0.1:8000/users/
```

![GET /users/](capturas/04_get_users.png)

---

### GET /users/{user_id} — Obtener usuario por ID

```http
GET http://127.0.0.1:8000/users/1
```

![GET /users/1](capturas/05_get_user_id.png)

---




### GET /users/?is_active=false — Filtrar por estado

```http
GET http://127.0.0.1:8000/users/?role=admin
```


![GET ?role=admin](capturas/06_get_filtro_activo.png)

---
### POST /users/ — Registrar nuevo usuario

```http
POST http://127.0.0.1:8000/users/
Content-Type: application/json

{
  "name": "Ana García",
  "email": "ana@devicesystems.com",
  "role": "user",
  "is_active": true
}
```

**Respuesta 201 Created:**
```json
{
  "id": 5,
  "name": "Ana García",
  "email": "ana@devicesystems.com",
  "role": "user",
  "is_active": true
}
```

---

## Validaciones y manejo de errores

### Error 409 — Email duplicado

Intentar registrar el mismo correo dos veces retorna:

```json
{
  "detail": "El correo 'ana@devicesystems.com' ya está registrado."
}
```
---

### Error 422 — Datos inválidos (Pydantic)

Enviar un nombre con menos de 3 caracteres retorna:

```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "String should have at least 3 characters",
      "type": "string_too_short"
    }
  ]
}
```

---

### Error 404 — Usuario no encontrado

```json
{
  "detail": "No existe un usuario con ID 99."
}
```


---
