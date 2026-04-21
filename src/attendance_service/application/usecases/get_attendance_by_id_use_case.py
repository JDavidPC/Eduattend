from ...application.ports.outbound.i_attendance_repository import IAttendanceRepository
from ...domain.exception import AttendanceNotFoundError
from ...domain.model.attendance import Attendance


class GetAttendanceByIdUseCase:
    def __init__(self, repository: IAttendanceRepository) -> None:
        self._repository = repository

    def execute(self, attendance_id: int) -> Attendance:
        attendance = self._repository.get_by_id(attendance_id)
        if attendance is None:
            raise AttendanceNotFoundError(
                f"No existe asistencia con id {attendance_id}."
            )
        return attendance
