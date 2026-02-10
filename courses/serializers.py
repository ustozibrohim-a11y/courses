from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Enrollment

User = get_user_model()


class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'role')


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'course', 'title', 'content', 'order', 'added_at')
        read_only_fields = ('added_at', 'course')


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'order', 'added_at')


class CourseSerializer(serializers.ModelSerializer):
    teacher_detail = UserBriefSerializer(source='teacher', read_only=True)
    lessons = LessonListSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            'id', 'name', 'description', 'teacher', 'teacher_detail',
            'added_at', 'is_active', 'lessons'
        )
        read_only_fields = ('added_at', 'teacher')


class CourseListSerializer(serializers.ModelSerializer):
    teacher_detail = UserBriefSerializer(source='teacher', read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'teacher', 'teacher_detail', 'added_at', 'is_active')


class EnrollmentSerializer(serializers.ModelSerializer):
    course_detail = CourseListSerializer(source='course', read_only=True)
    student_detail = UserBriefSerializer(source='student', read_only=True)

    class Meta:
        model = Enrollment
        fields = ('id', 'student', 'course', 'enrolled_at', 'is_active', 'course_detail', 'student_detail')
        read_only_fields = ('enrolled_at', 'student')
