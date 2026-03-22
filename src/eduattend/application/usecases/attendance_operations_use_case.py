from ...application.ports.inbound.i_attendance_operations_use_case import (
    IAttendanceOperationsUseCase,
)
from ...application.ports.outbound.i_attendance_repository import IAttendanceRepository
from ...domain.model.attendance import Attendance
from .delete_attendance_use_case import DeleteAttendanceUseCase
from .get_attendance_by_id_use_case import GetAttendanceByIdUseCase
from .list_attendances_use_case import ListAttendancesUseCase
from .register_attendance_command import RegisterAttendanceCommand
from .register_attendance_use_case import RegisterAttendanceUseCase
from .update_attendance_command import UpdateAttendanceCommand
from .update_attendance_use_case import UpdateAttendanceUseCase


class AttendanceOperationsUseCase(IAttendanceOperationsUseCase):
    def __init__(self, repository: IAttendanceRepository) -> None:
        self._register_use_case = RegisterAttendanceUseCase(repository)
        self._list_use_case = ListAttendancesUseCase(repository)
        self._get_by_id_use_case = GetAttendanceByIdUseCase(repository)
        self._update_use_case = UpdateAttendanceUseCase(repository)
        self._delete_use_case = DeleteAttendanceUseCase(repository)

    def register_attendance(self, command: RegisterAttendanceCommand) -> Attendance:
        return self._register_use_case.execute(command)

    def list_attendances(self) -> list[Attendance]:
        return self._list_use_case.execute()

    def get_attendance_by_id(self, attendance_id: int) -> Attendance:
        return self._get_by_id_use_case.execute(attendance_id)

    def update_attendance(
        self,
        attendance_id: int,
        command: UpdateAttendanceCommand,
    ) -> Attendance:
        return self._update_use_case.execute(attendance_id, command)

    def delete_attendance(self, attendance_id: int) -> None:
        self._delete_use_case.execute(attendance_id)
