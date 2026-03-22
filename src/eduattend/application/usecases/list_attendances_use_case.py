from ...application.ports.outbound.i_attendance_repository import IAttendanceRepository
from ...domain.model.attendance import Attendance


class ListAttendancesUseCase:
    def __init__(self, repository: IAttendanceRepository) -> None:
        self._repository = repository

    def execute(self) -> list[Attendance]:
        return self._repository.list_all()
