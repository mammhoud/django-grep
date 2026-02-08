import logging

from django.utils import timezone

logger = logging.getLogger(__name__)


def should_be_student(user):
    """Determine if the user should have a Student profile."""
    email = (user.email or "").lower()
    if "@student." in email or ".edu" in email:
        return True
    return user.groups.filter(name__in=["Students", "Learners"]).exists()


def should_be_instructor(user):
    """Determine if the user should have an Instructor profile."""
    email = (user.email or "").lower()
    if any(x in email for x in ["@prof.", "@faculty.", "@instructor."]):
        return True
    return user.groups.filter(name__in=["Instructors", "Teachers", "Faculty"]).exists()


def create_role_specific_profiles(user, profile, person):
    """Create role-specific records based on user type (student/instructor)."""
    try:
        from apps.pages.models import Instructor, Student

        from .utils import should_be_instructor, should_be_student

        if should_be_student(user):
            Student.objects.create(
                person=person,
                user=user,
                enrollment_id=f"STU{user.id:06d}",
                student_status=Student.StudentStatus.ACTIVE,
                enrollment_date=timezone.now().date(),
                is_active=True,
            )
            logger.info(f"Created student profile for: {user.username}")

        elif should_be_instructor(user):
            Instructor.objects.create(
                person=person,
                user=user,
                employee_id=f"INST{user.id:06d}",
                employment_status=Instructor.EmploymentStatus.FULL_TIME,
                hire_date=timezone.now().date(),
                is_active=True,
            )
            logger.info(f"Created instructor profile for: {user.username}")

    except Exception as e:
        logger.error(f"Error creating role-specific profile for {user.username}: {e!s}")
