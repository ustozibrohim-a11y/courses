from rest_framework import permissions


class IsTeacher(permissions.BasePermission):
    """Faqat Teacher rolida bo'lgan foydalanuvchi."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'Teacher'


class IsCourseTeacher(permissions.BasePermission):
    """Kurs egasi (teacher) bo'lgan foydalanuvchi."""

    def has_object_permission(self, request, view, obj):
        course = getattr(obj, 'course', obj)
        return course.teacher_id == request.user.id


class IsEnrolledStudent(permissions.BasePermission):
    """Kursga yozilgan Student."""

    def has_object_permission(self, request, view, obj):
        from .models import Enrollment
        if request.user.role != 'Student':
            return False
        course = getattr(obj, 'course', obj)
        return Enrollment.objects.filter(student=request.user, course=course, is_active=True).exists()
