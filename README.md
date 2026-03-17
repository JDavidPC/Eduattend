# EduAttend API - Arquitectura Hexagonal

API en Flask para el caso de negocio de control de asistencia:

- Un estudiante solo puede registrar asistencia una vez por clase por dia.
- Si intenta registrarse nuevamente, la API responde con conflicto de negocio (HTTP 409).

## Estructura de carpetas

```
registro-notas-AH/
  run.py
  requirements.txt
  src/
    eduattend/
      app.py                         # Configuracion Flask y wiring
      domain/
        entities.py                  # Entidades del dominio
        exceptions.py                # Excepciones de negocio
        ports.py                     # Puertos (interfaces)
      application/
        commands.py                  # DTO/comandos
        use_cases.py                 # Casos de uso
      infrastructure/
        db.py                        # Configuracion SQLAlchemy
        models.py                    # Modelos de persistencia
        repositories.py              # Adaptador de salida (repo SQLAlchemy)
        http.py                      # Adaptador de entrada (Flask endpoints)
```

## Instalacion y ejecucion

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
  "attendance_date": "2026-03-16"
}
```

Si `attendance_date` no se envia, toma la fecha actual.

### Listar asistencias

- `GET /api/v1/attendance`

## cURL de prueba

Registrar asistencia:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/attendance \
  -H "Content-Type: application/json" \
  -d "{\"student_id\":\"S1\",\"course_id\":\"MAT101\",\"class_session_id\":\"CLASE-01\",\"attendance_date\":\"2026-03-16\"}"
```

Intentar duplicado (debe responder 409):

```bash
curl -X POST http://127.0.0.1:5000/api/v1/attendance \
  -H "Content-Type: application/json" \
  -d "{\"student_id\":\"S1\",\"course_id\":\"MAT101\",\"class_session_id\":\"CLASE-01\",\"attendance_date\":\"2026-03-16\"}"
```

Listar:

```bash
curl http://127.0.0.1:5000/api/v1/attendance
```
