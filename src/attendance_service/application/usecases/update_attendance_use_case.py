from ...application.ports.outbound.i_attendance_repository import IAttendanceRepository
from ...domain.exception import AttendanceNotFoundError, DuplicateAttendanceError
from ...domain.model.attendance import Attendance
from .update_attendance_command import UpdateAttendanceCommand


class UpdateAttendanceUseCase:
    def __init__(self, repository: IAttendanceRepository) -> None:
        self._repository = repository

    def execute(self, attendance_id: int, command: UpdateAttendanceCommand) -> Attendance:
        current = self._repository.get_by_id(attendance_id)
        if current is None:
            raise AttendanceNotFoundError(
                f"No existe asistencia con id {attendance_id}."
            )

        is_key_changed = (
            current.student_id != command.student_id
            or current.course_id != command.course_id
            or current.class_session_id != command.class_session_id
            or current.attendance_date != command.attendance_date
        )

        if is_key_changed and self._repository.exists_for_student_class_day(
            student_id=command.student_id,
            course_id=command.course_id,
            class_session_id=command.class_session_id,
            attendance_date=command.attendance_date,
        ):
            raise DuplicateAttendanceError(
                "El estudiante ya registro asistencia para esta clase en esta fecha."
            )

        updated = Attendance(
            id=current.id,
            student_id=command.student_id,
            course_id=command.course_id,
            class_session_id=command.class_session_id,
            attendance_date=command.attendance_date,
            registered_at=current.registered_at,
        )
        return self._repository.update(updated)
