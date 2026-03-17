from datetime import datetime

from .commands import RegisterAttendanceCommand
from ..domain.entities import Attendance
from ..domain.exceptions import DuplicateAttendanceError
from ..domain.ports import AttendanceRepository


class RegisterAttendanceUseCase:
    def __init__(self, repository: AttendanceRepository) -> None:
        self._repository = repository

    def execute(self, command: RegisterAttendanceCommand) -> Attendance:
        already_registered = self._repository.exists_for_student_class_day(
            student_id=command.student_id,
            course_id=command.course_id,
            class_session_id=command.class_session_id,
            attendance_date=command.attendance_date,
        )

        if already_registered:
            raise DuplicateAttendanceError(
                "El estudiante ya registró asistencia para esta clase en esta fecha."
            )

        attendance = Attendance(
            student_id=command.student_id,
            course_id=command.course_id,
            class_session_id=command.class_session_id,
            attendance_date=command.attendance_date,
            registered_at=datetime.utcnow(),
        )
        return self._repository.save(attendance)


class ListAttendancesUseCase:
    def __init__(self, repository: AttendanceRepository) -> None:
        self._repository = repository

    def execute(self) -> list[Attendance]:
        return self._repository.list_all()
