from .route_advices import advices_bp
from .route_attendance import attendance_bp
from .route_exam import exam_bp
from .route_classes import classes_bp
from .route_exam_types import exam_types_bp
from .route_marks import marks_bp
from .route_roles import roles_bp
from .route_professor import professor_bp
from .route_students import students_bp
from .route_users import users_bp
from .route_teams import teams_bp
from .route_assistant import assistant_bp

__all__ = ["advices_bp", "attendance_bp", "exam_bp", "classes_bp", "exam_types_bp", "marks_bp", "roles_bp", "professor_bp", "students_bp", "users_bp", "teams_bp", "assistant_bp"]