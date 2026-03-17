from datetime import date
from http import HTTPStatus

from flask import Blueprint, jsonify, request

from ..application.commands import RegisterAttendanceCommand
from ..application.use_cases import ListAttendancesUseCase, RegisterAttendanceUseCase
from ..domain.entities import Attendance


def create_attendance_blueprint(
    register_use_case: RegisterAttendanceUseCase,
    list_use_case: ListAttendancesUseCase,
) -> Blueprint:
    blueprint = Blueprint("attendance", __name__)

    @blueprint.post("/api/v1/attendance")
    def register_attendance():
        """
        Registrar asistencia
        ---
        tags:
            - Attendance
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        required:
                            - student_id
                            - course_id
                            - class_session_id
                        properties:
                            student_id:
                                type: string
                                example: S1
                            course_id:
                                type: string
                                example: MAT101
                            class_session_id:
                                type: string
                                example: CLASE-01
                            attendance_date:
                                type: string
                                format: date
                                example: 2026-03-16
        responses:
            201:
                description: Asistencia registrada
            400:
                description: Error de validacion
            409:
                description: Regla de negocio violada por duplicado
        """
        payload = request.get_json(silent=True) or {}

        required_fields = ["student_id", "course_id", "class_session_id"]
        missing = [field for field in required_fields if not payload.get(field)]
        if missing:
            return (
                jsonify(
                    {
                        "error": "validation_error",
                        "message": f"Campos requeridos faltantes: {', '.join(missing)}",
                    }
                ),
                HTTPStatus.BAD_REQUEST,
            )

        raw_date = payload.get("attendance_date")
        try:
            attendance_date = date.fromisoformat(raw_date) if raw_date else date.today()
        except ValueError:
            return (
                jsonify(
                    {
                        "error": "validation_error",
                        "message": "attendance_date debe tener formato YYYY-MM-DD.",
                    }
                ),
                HTTPStatus.BAD_REQUEST,
            )

        command = RegisterAttendanceCommand(
            student_id=str(payload["student_id"]),
            course_id=str(payload["course_id"]),
            class_session_id=str(payload["class_session_id"]),
            attendance_date=attendance_date,
        )
        attendance = register_use_case.execute(command)
        return jsonify(_attendance_to_dict(attendance)), HTTPStatus.CREATED

    @blueprint.get("/api/v1/attendance")
    def list_attendance():
        """
        Listar asistencias
        ---
        tags:
            - Attendance
        responses:
            200:
                description: Lista de asistencias registradas
        """
        attendances = list_use_case.execute()
        return jsonify([_attendance_to_dict(attendance) for attendance in attendances])

    return blueprint


def _attendance_to_dict(attendance: Attendance) -> dict:
    return {
        "id": attendance.id,
        "student_id": attendance.student_id,
        "course_id": attendance.course_id,
        "class_session_id": attendance.class_session_id,
        "attendance_date": attendance.attendance_date.isoformat(),
        "registered_at": attendance.registered_at.isoformat() + "Z",
    }
