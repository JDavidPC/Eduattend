from ...application.ports.outbound.i_attendance_repository import IAttendanceRepository
from ...domain.exception import AttendanceNotFoundError


class DeleteAttendanceUseCase:
    def __init__(self, repository: IAttendanceRepository) -> None:
        self._repository = repository

    def execute(self, attendance_id: int) -> None:
        was_deleted = self._repository.delete_by_id(attendance_id)
        if not was_deleted:
            raise AttendanceNotFoundError(
                f"No existe asistencia con id {attendance_id}."
            )
