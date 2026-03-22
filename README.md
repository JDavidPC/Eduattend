# EduAttend API - Arquitectura Hexagonal

API en Flask para el caso de negocio de control de asistencia:

- Un estudiante solo puede registrar asistencia una vez por clase por día.
- Si intenta registrarse nuevamente, la API responde con conflicto de negocio (HTTP 409).

## Estructura de carpetas

```text
registro-notas-AH/
  run.py
  requirements.txt
  src/
    eduattend/
      app.py                          # Configuración Flask y wiring
      application/
        ports/                        # Puertos (Interfaces de entrada y salida)
        usecases/                     # Casos de uso de la aplicación
      domain/
        exception/                    # Excepciones de negocio del dominio
        model/                        # Entidades y modelos del dominio
        service/                      # Servicios de dominio
      infrastructure/
        adapters/                     # Adaptadores de entrada (HTTP/Flask) y salida (Repositorios/SQLAlchemy)
        config/                       # Configuración de base de datos y variables de entorno
        mappers/                      # Mapeadores entre entidades de dominio y modelos de persistencia
```

## Instalación y ejecución

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python run.py
```

Base URL local: `http://127.0.0.1:5000`

## Endpoints

### Health

- `GET /health`

### Registrar asistencia

- `POST /api/v1/attendance`
- Body JSON:

```json
{
  "student_id": "S1",
  "course_id": "MAT101",
  "class_session_id": "CLASE-01",
  "attendance_date": "2026-03-22"
}
```

Si `attendance_date` no se envía, toma la fecha actual.

### Listar asistencias

- `GET /api/v1/attendance`

## cURL de prueba

Registrar asistencia:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/attendance \
  -H "Content-Type: application/json" \
  -d "{\"student_id\":\"S1\",\"course_id\":\"MAT101\",\"class_session_id\":\"CLASE-01\",\"attendance_date\":\"2026-03-22\"}"
```

Intentar duplicado (debe responder 409):

```bash
curl -X POST http://127.0.0.1:5000/api/v1/attendance \
  -H "Content-Type: application/json" \
  -d "{\"student_id\":\"S1\",\"course_id\":\"MAT101\",\"class_session_id\":\"CLASE-01\",\"attendance_date\":\"2026-03-22\"}"
```

Listar:

```bash
curl http://127.0.0.1:5000/api/v1/attendance
```
