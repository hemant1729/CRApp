from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('register/', views.register),
    path('admin/', views.admin_home),
    path('admin/program/', views.admin_program),
    path('admin/dept/', views.admin_dept),
    path('admin/course/', views.admin_course),
    path('admin/instr/', views.admin_instr),
    path('admin/sem/', views.admin_sem),
    path('admin/timeslot/', views.admin_timeslot),
    path('admin/tag/', views.admin_tags),
    path('admin/course_tags/', views.admin_course_tags),
    path('admin/course_sem/', views.admin_course_sem),
    path('admin/grade/', views.admin_grade),
    path('student/', views.student_home),
    path('student/interests/', views.student_interests),
    path('student/courses/', views.student_courses),
    path('student/reviews/', views.student_reviews),
    path('view_reviews/', views.view_reviews),
]
