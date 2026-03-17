import os
from http import HTTPStatus

from flask import Flask, jsonify
from flasgger import Swagger

from .application.use_cases import ListAttendancesUseCase, RegisterAttendanceUseCase
from .domain.exceptions import DuplicateAttendanceError
from .infrastructure.db import build_session_factory
from .infrastructure.http import create_attendance_blueprint
from .infrastructure.repositories import SqlAlchemyAttendanceRepository


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    app.config["SWAGGER"] = {
        "title": "EduAttend API",
        "uiversion": 3,
        "openapi": "3.0.2",
    }
    Swagger(app)

    database_url = os.getenv("DATABASE_URL", "sqlite:///eduattend.db")
    session_factory = build_session_factory(database_url)

    repository = SqlAlchemyAttendanceRepository(session_factory)
    register_use_case = RegisterAttendanceUseCase(repository)
    list_use_case = ListAttendancesUseCase(repository)

    app.register_blueprint(
        create_attendance_blueprint(
            register_use_case=register_use_case,
            list_use_case=list_use_case,
        )
    )

    @app.get("/health")
    def health_check():
        return jsonify({"status": "ok"}), HTTPStatus.OK

    @app.errorhandler(DuplicateAttendanceError)
    def handle_duplicate_attendance(error: DuplicateAttendanceError):
        return (
            jsonify(
                {
                    "error": "business_rule_violation",
                    "message": str(error),
                }
            ),
            HTTPStatus.CONFLICT,
        )

    return app
