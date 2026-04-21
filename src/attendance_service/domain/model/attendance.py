from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass(frozen=True)
class Attendance:
    student_id: str
    course_id: str
    class_session_id: str
    attendance_date: date
    registered_at: datetime
    id: Optional[int] = None
