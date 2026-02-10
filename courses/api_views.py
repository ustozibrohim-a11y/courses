from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Course, Lesson, Enrollment
from .serializers import (
    CourseSerializer, CourseListSerializer,
    LessonSerializer, LessonListSerializer,
    EnrollmentSerializer,
)
from .permissions import IsTeacher, IsCourseTeacher, IsEnrolledStudent


# ——— Course ———
class CourseListCreateView(generics.ListCreateAPIView):
    """Kurslar ro'yxati (barcha). Kurs yaratish faqat Teacher."""
    queryset = Course.objects.filter(is_active=True).select_related('teacher').prefetch_related('lessons')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return CourseListSerializer if self.request.method == 'GET' else CourseSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsTeacher()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Kurs detail, tahrirlash, o'chirish – faqat Teacher (egasi)."""
    queryset = Course.objects.filter(is_active=True).select_related('teacher').prefetch_related('lessons')
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        perms = [IsAuthenticated()]
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            perms.append(IsCourseTeacher())
        return perms

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


# ——— Lesson ———
class LessonListCreateView(generics.ListCreateAPIView):
    """Darslar ro'yxati (kurs bo'yicha). Dars qo'shish faqat Teacher (kurs egasi)."""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, pk=course_id, is_active=True)
        return Lesson.objects.filter(course=course).order_by('order', 'added_at')

    def get_serializer_class(self):
        return LessonListSerializer if self.request.method == 'GET' else LessonSerializer

    def get_permissions(self):
        perms = [IsAuthenticated()]
        if self.request.method == 'POST':
            perms.append(IsTeacher())
        return perms

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['course_id'] = self.kwargs.get('course_id')
        return ctx

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'], is_active=True)
        if course.teacher_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Faqat kurs egasi dars qo\'sha oladi.')
        serializer.save(course=course)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Dars detail, tahrirlash, o'chirish – Teacher (egasi). Ko'rish – kursga yozilgan Student yoki Teacher."""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Lesson.objects.select_related('course')

    def get_object(self):
        qs = self.get_queryset()
        return get_object_or_404(qs, pk=self.kwargs['pk'])

    def get_permissions(self):
        perms = [IsAuthenticated()]
        obj = self.get_object()
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            if obj.course.teacher_id != self.request.user.id:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied('Faqat kurs egasi darsni tahrirlaydi/o\'chiradi.')
        return perms


# ——— Enrollment ———
class EnrollmentListCreateView(generics.ListCreateAPIView):
    """O'z kurslarini ko'rish. Kursga yozilish – faqat Student."""
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(
            student=self.request.user, is_active=True
        ).select_related('course', 'course__teacher').order_by('-enrolled_at')

    def get_permissions(self):
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied
        if self.request.user.role != 'Student':
            raise PermissionDenied('Faqat talaba kursga yozilishi mumkin.')
        course_id = self.request.data.get('course')
        course = get_object_or_404(Course, pk=course_id, is_active=True)
        if Enrollment.objects.filter(student=self.request.user, course=course).exists():
            raise PermissionDenied('Siz allaqachon ushbu kursga yozilgansiz.')
        serializer.save(student=self.request.user, course=course)


class EnrollmentLeaveView(generics.GenericAPIView):
    """Kursdan chiqish – Student o'z yozilishini is_active=False qiladi."""
    permission_classes = [IsAuthenticated]
    queryset = Enrollment.objects.all()

    def post(self, request, pk):
        enrollment = get_object_or_404(Enrollment, pk=pk, student=request.user)
        enrollment.is_active = False
        enrollment.save()
        return Response({'detail': 'Kursdan muvaffaqiyatli chiqildi.'}, status=status.HTTP_200_OK)
