# device_systems — API REST con FastAPI + SQLAlchemy + Alembic

API REST para la gestión de **usuarios**, **dispositivos** y **préstamos** del sistema `device_systems` con relaciones entre modelos, migraciones con Alembic y consultas con joins.

---

## Estructura del proyecto

![Estructura del proyecto](capturas/estructura.png)

---

## Migraciones con Alembic

Al aplicar las migraciones, Alembic crea automáticamente el archivo `device_systems.db` con las tablas `users`, `devices` y `loans`.

### Aplicar migración inicial

```bash
python -m alembic upgrade head
```

![alembic upgrade head](capturas/alembic_upgrade.png)

### Historial de migraciones

```bash
python -m alembic history
```

![alembic history](capturas/alembic_history.png)

---

## Pruebas de endpoints

### POST /users — Crear usuario
![POST crear usuario](capturas/post_user_ok.png)

### POST /devices — Crear dispositivo
![POST crear dispositivo](capturas/post_device_ok.png)

### POST /devices — Serial duplicado (400)
![POST serial duplicado](capturas/post_device_duplicado.png)

### GET /devices — Listar dispositivos
![GET dispositivos](capturas/get_devices.png)

### GET /devices?device_type=laptop — Filtrar por tipo
![Filtro tipo dispositivo](capturas/get_devices_type.png)

### GET /devices?is_available=true — Filtrar disponibles
![Filtro disponibles](capturas/get_devices_available.png)

### GET /devices?brand=lenovo — Filtrar por marca
![Filtro marca](capturas/get_devices_brand.png)

### GET /devices?search=thinkpad — Búsqueda avanzada
![Búsqueda](capturas/get_devices_search.png)

### POST /loans — Crear préstamo
![POST crear préstamo](capturas/post_loan_ok.png)

### POST /loans — Dispositivo no disponible (409)
![POST dispositivo no disponible](capturas/post_loan_conflict.png)

### GET /loans — Listar préstamos
![GET préstamos](capturas/get_loans.png)

### GET /loans/details — Préstamos con detalle (join)
![GET préstamos detalle](capturas/get_loans_details.png)

### GET /loans?status=active — Filtrar por estado
![Filtro estado](capturas/get_loans_status.png)

### GET /loans?device_type=laptop — Filtrar por tipo de dispositivo
![Filtro tipo en préstamos](capturas/get_loans_device_type.png)

### GET /loans/user/{user_id} — Préstamos de un usuario
![Préstamos por usuario](capturas/get_loans_by_user.png)

### PATCH /loans/{id}/return — Devolver dispositivo
![Devolución](capturas/patch_loan_return.png)

### GET /devices/{id} tras devolución — Verificar disponibilidad
![Dispositivo disponible tras devolución](capturas/get_device_after_return.png)

### GET /loans/device/{device_id} — Historial de préstamos del dispositivo
![Historial préstamos dispositivo](capturas/get_loans_by_device.png)

---

## Errores controlados

| Caso | Código |
|------|:------:|
| Usuario no encontrado | 404 Not Found |
| Dispositivo no encontrado | 404 Not Found |
| Préstamo no encontrado | 404 Not Found |
| Email duplicado | 400 Bad Request |
| Número de serie duplicado | 400 Bad Request |
| Dispositivo no disponible | 409 Conflict |
| Préstamo ya devuelto | 409 Conflict |
| Datos inválidos | 422 Unprocessable Entity |

---

## Relaciones entre modelos

| Relación | Tipo | Implementación |
|----------|------|----------------|
| User → Loan | One-to-Many | `relationship("Loan", back_populates="user")` |
| Device → Loan | One-to-Many | `relationship("Loan", back_populates="device")` |
| Loan → User | Many-to-One | `ForeignKey("users.id")` |
| Loan → Device | Many-to-One | `ForeignKey("devices.id")` |

Un usuario puede tener muchos préstamos. Un dispositivo puede aparecer en muchos préstamos históricos. Cada préstamo pertenece siempre a un usuario y un dispositivo existentes.

---

## Diferencia entre modelo SQLAlchemy y schema Pydantic

| | Modelo SQLAlchemy | Schema Pydantic |
|---|---|---|
| **¿Qué es?** | Representa la tabla en la base de datos | Representa los datos que entran y salen de la API |
| **¿Para qué sirve?** | Hablar con la base de datos via ORM | Validar y serializar datos HTTP |
| **¿Dónde vive?** | `app/models/` | `app/schemas/` |
| **Hereda de** | `Base` (declarative_base) | `BaseModel` (Pydantic) |
| **Ejemplo** | `Column(String, nullable=False)` | `Field(..., min_length=3)` |

En resumen: el modelo SQLAlchemy le habla a la base de datos, el schema Pydantic le habla al cliente HTTP. Son capas separadas con responsabilidades distintas.

---

## Reflexión final

Evolucionar una API con relaciones entre modelos, migraciones y consultas con joins representa un salto cualitativo en el desarrollo backend. Las migraciones con Alembic permiten versionar los cambios estructurales de la base de datos de forma controlada, similar a como Git versiona el código fuente: cada cambio queda registrado, es reversible y trazable.

Las relaciones entre `User`, `Device` y `Loan` mediante `ForeignKey` y `relationship` garantizan la integridad referencial del sistema: no puede existir un préstamo sin un usuario y un dispositivo válidos. Esto traslada la lógica de negocio al nivel de la base de datos, no solo a la aplicación.

Las consultas con joins eliminan múltiples roundtrips a la base de datos y permiten construir respuestas ricas combinando información de varias tablas en una sola operación eficiente, lo que se traduce directamente en mejor rendimiento y código más limpio.

## Link YouTube proyecto final v1: