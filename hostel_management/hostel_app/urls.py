# hostel_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.home, name='home'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('students/<int:student_id>/delete/', views.delete_student, name='delete_student'),

    # Rooms
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.add_room, name='add_room'),
    path('rooms/<int:room_id>/edit/', views.edit_room, name='edit_room'),
    path('rooms/<int:room_id>/delete/', views.delete_room, name='delete_room'),

    # Attendance
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),

    # Rules
    path('rules/', views.rules_list, name='rules_list'),
    path('rules/add/', views.add_rule, name='add_rule'),
    path('rules/<int:rule_id>/edit/', views.edit_rule, name='edit_rule'),
    path('rules/<int:rule_id>/delete/', views.delete_rule, name='delete_rule'),
]