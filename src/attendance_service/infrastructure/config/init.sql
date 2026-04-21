-- src/attendance_service/infrastructure/config/init.sql
CREATE TABLE IF NOT EXISTS attendances (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    course_id VARCHAR(50) NOT NULL,
    class_session_id VARCHAR(50) NOT NULL,
    attendance_date DATE NOT NULL,
    registered_at TIMESTAMP NOT NULL,
    CONSTRAINT uq_attendance_student_class_day UNIQUE (
        student_id,
        course_id,
        class_session_id,
        attendance_date
    )
);
