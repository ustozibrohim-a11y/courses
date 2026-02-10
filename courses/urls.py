from django.urls import path, include
from . import api_views

urlpatterns = [
    path('courses/', api_views.CourseListCreateView.as_view(), name='api_course_list_create'),
    path('courses/<int:pk>/', api_views.CourseDetailView.as_view(), name='api_course_detail'),
    path('courses/<int:course_id>/lessons/', api_views.LessonListCreateView.as_view(), name='api_lesson_list_create'),
    path('lessons/<int:pk>/', api_views.LessonDetailView.as_view(), name='api_lesson_detail'),
    path('enrollments/', api_views.EnrollmentListCreateView.as_view(), name='api_enrollment_list_create'),
    path('enrollments/<int:pk>/leave/', api_views.EnrollmentLeaveView.as_view(), name='api_enrollment_leave'),
]
