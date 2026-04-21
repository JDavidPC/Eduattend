# src/attendance_service/domain/model/absence_event.py
from dataclasses import dataclass


@dataclass(frozen=True)
class AbsenceEvent:
    event: str
    student_id: str
    student_email: str
    course_id: str
    count: int
    timestamp: str

    def __post_init__(self) -> None:
        if self.event != "ABSENCE_LIMIT_REACHED":
            raise ValueError("event debe ser ABSENCE_LIMIT_REACHED")
