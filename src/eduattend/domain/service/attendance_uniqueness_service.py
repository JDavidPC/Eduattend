from datetime import date
from typing import Protocol

from ..exception.business_rule_violation import DuplicateAttendanceError


class IAttendanceUniquenessChecker(Protocol):
    def exists_for_student_class_day(
        self,
        student_id: str,
        course_id: str,
        class_session_id: str,
        attendance_date: date,
    ) -> bool: ...


class AttendanceUniquenessService:
    def __init__(self, repository: IAttendanceUniquenessChecker) -> None:
        self._repository = repository

    def ensure_attendance_not_registered(
        self,
        student_id: str,
        course_id: str,
        class_session_id: str,
        attendance_date: date,
    ) -> None:
        already_registered = self._repository.exists_for_student_class_day(
            student_id=student_id,
            course_id=course_id,
            class_session_id=class_session_id,
            attendance_date=attendance_date,
        )
        if already_registered:
            raise DuplicateAttendanceError(
                "El estudiante ya registro asistencia para esta clase en esta fecha."
            )
