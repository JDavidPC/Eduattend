from abc import ABC, abstractmethod

from ....domain.model.attendance import Attendance
from ...usecases.register_attendance_command import RegisterAttendanceCommand
from ...usecases.update_attendance_command import UpdateAttendanceCommand


class IAttendanceOperationsUseCase(ABC):
    @abstractmethod
    def register_attendance(self, command: RegisterAttendanceCommand) -> Attendance:
        raise NotImplementedError

    @abstractmethod
    def list_attendances(self) -> list[Attendance]:
        raise NotImplementedError

    @abstractmethod
    def get_attendance_by_id(self, attendance_id: int) -> Attendance:
        raise NotImplementedError

    @abstractmethod
    def update_attendance(
        self,
        attendance_id: int,
        command: UpdateAttendanceCommand,
    ) -> Attendance:
        raise NotImplementedError

    @abstractmethod
    def delete_attendance(self, attendance_id: int) -> None:
        raise NotImplementedError
