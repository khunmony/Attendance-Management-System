import enum


class Role(str, enum.Enum):
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"


class AttendanceStatus(str, enum.Enum):
    PRESENT = "PRESENT"
    LATE = "LATE"
    ABSENT = "ABSENT"
    EXCUSED = "EXCUSED"
    LEFT_EARLY = "LEFT_EARLY"


class MarkMethod(str, enum.Enum):
    TEACHER = "TEACHER"  # teacher marked the roll
    QR = "QR"  # student scanned the session QR
    GEOFENCE = "GEOFENCE"  # student checked in inside the school radius
    ADMIN_OVERRIDE = "ADMIN_OVERRIDE"


class SessionStatus(str, enum.Enum):
    SCHEDULED = "SCHEDULED"
    OPEN = "OPEN"  # attendance being taken
    CLOSED = "CLOSED"  # attendance finalized
    CANCELLED = "CANCELLED"


class EnrollmentStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    WITHDRAWN = "WITHDRAWN"
    GRADUATED = "GRADUATED"


class ExcuseReason(str, enum.Enum):
    SICK = "SICK"
    FAMILY = "FAMILY"
    APPOINTMENT = "APPOINTMENT"
    OTHER = "OTHER"


class ExcuseStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


class NotificationType(str, enum.Enum):
    EXCUSE_SUBMITTED = "EXCUSE_SUBMITTED"
    EXCUSE_APPROVED = "EXCUSE_APPROVED"
    EXCUSE_REJECTED = "EXCUSE_REJECTED"
    MARKED_ABSENT = "MARKED_ABSENT"
    LOW_ATTENDANCE = "LOW_ATTENDANCE"
    ATTENDANCE_OVERRIDDEN = "ATTENDANCE_OVERRIDDEN"
    SYSTEM = "SYSTEM"
