from abc import ABC, abstractmethod
from datetime import date

from .entities import Attendance


class AttendanceRepository(ABC):
    @abstractmethod
    def exists_for_student_class_day(
        self,
        student_id: str,
        course_id: str,
        class_session_id: str,
        attendance_date: date,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def save(self, attendance: Attendance) -> Attendance:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[Attendance]:
        raise NotImplementedError
