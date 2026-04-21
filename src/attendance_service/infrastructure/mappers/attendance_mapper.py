from ..adapters.outbound.attendance_orm_model import AttendanceOrmModel
from ...domain.model.attendance import Attendance


def attendance_from_orm(model: AttendanceOrmModel) -> Attendance:
    return Attendance(
        id=model.id,
        student_id=model.student_id,
        course_id=model.course_id,
        class_session_id=model.class_session_id,
        attendance_date=model.attendance_date,
        registered_at=model.registered_at,
    )


def orm_from_attendance(attendance: Attendance) -> AttendanceOrmModel:
    return AttendanceOrmModel(
        student_id=attendance.student_id,
        course_id=attendance.course_id,
        class_session_id=attendance.class_session_id,
        attendance_date=attendance.attendance_date,
        registered_at=attendance.registered_at,
    )
