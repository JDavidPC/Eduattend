from datetime import datetime

from ...application.ports.outbound.i_attendance_repository import IAttendanceRepository
from ...domain.model.attendance import Attendance
from ...domain.service.attendance_uniqueness_service import AttendanceUniquenessService
from .register_attendance_command import RegisterAttendanceCommand


class RegisterAttendanceUseCase:
    def __init__(self, repository: IAttendanceRepository) -> None:
        self._repository = repository
        self._uniqueness_service = AttendanceUniquenessService(repository)

    def execute(self, command: RegisterAttendanceCommand) -> Attendance:
        self._uniqueness_service.ensure_attendance_not_registered(
            student_id=command.student_id,
            course_id=command.course_id,
            class_session_id=command.class_session_id,
            attendance_date=command.attendance_date,
        )

        attendance = Attendance(
            student_id=command.student_id,
            course_id=command.course_id,
            class_session_id=command.class_session_id,
            attendance_date=command.attendance_date,
            registered_at=datetime.utcnow(),
        )
        return self._repository.save(attendance)
