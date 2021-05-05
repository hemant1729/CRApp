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
    path('student/', views.student_test),
]