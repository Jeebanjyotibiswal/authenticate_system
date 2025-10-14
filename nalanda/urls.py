from django.contrib import admin
from django.urls import path
from home import views as home_views
from students import views as student_views
from teachers import views as teacher_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Home pages
    path('', home_views.index, name='index'),
    # path('about/', home_views.about, name='about'),

    # Student Registration & Dashboard
    path('student/register/', student_views.student_register, name='student_register'),
    path('student/login/', student_views.student_login, name='student_login'),
    path('student/dashboard/', student_views.student_dashboard, name='student_dashboard'),

    # Teacher Registration & Dashboard
    path('teacher/register/', teacher_views.teacher_register, name='teacher_register'),
    path('teacher/login/', teacher_views.teacher_login, name='teacher_login'),
    path('teacher/dashboard/', teacher_views.teacher_dashboard, name='teacher_dashboard'),

    # Login / Logout (shared)
    path('login/', student_views.student_login, name='login'),  # shared login
    path('logout/', student_views.logout_view, name='logout'),
    path('logout/', teacher_views.teacher_logout, name='teacher_logout'),
    path('logout/', student_views.logout_view, name='logout'),
    # Password Reset
    path('student/password_reset/', student_views.student_password_change, name='student_password_change'),
    path('teacher/password_reset/', teacher_views.teacher_password_change, name='teacher_password_change'),
]
