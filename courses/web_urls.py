from django.urls import path
from . import web_views

urlpatterns = [
    path('', web_views.home_view, name='home'),
    path('courses/', web_views.course_list_view, name='course_list'),
    path('courses/create/', web_views.course_create_view, name='course_create'),
    path('courses/<int:pk>/', web_views.course_detail_view, name='course_detail'),
    path('courses/<int:pk>/edit/', web_views.course_edit_view, name='course_edit'),
    path('courses/<int:course_id>/lessons/add/', web_views.lesson_add_view, name='lesson_add'),
    path('lessons/<int:pk>/edit/', web_views.lesson_edit_view, name='lesson_edit'),
    path('lessons/<int:pk>/delete/', web_views.lesson_delete_view, name='lesson_delete'),
    path('courses/<int:course_id>/enroll/', web_views.enroll_view, name='enroll'),
    path('courses/<int:course_id>/leave/', web_views.leave_view, name='leave'),
    path('courses/<int:pk>/students/', web_views.course_students, name='course_students'),
    path('dashboard/', web_views.dashboard_view, name='dashboard'),
    path('login/', web_views.login_view, name='login'),
    path('register/', web_views.register_view, name='register'),
    path('logout/', web_views.logout_view, name='logout'),
]
