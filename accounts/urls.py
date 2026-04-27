from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    student_dashboard,
    admin_dashboard,
    view_application,
    approve_application,
    reject_application,
)

urlpatterns = [
    path(
        'register/',
        register_view,
        name='register'
    ),

    path(
        'login/',
        login_view,
        name='login'
    ),

    path(
        'logout/',
        logout_view,
        name='logout'
    ),

    path(
        'dashboard/',
        student_dashboard,
        name='student_dashboard'
    ),

    path(
        'admin-dashboard/',
        admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'view-application/<int:bus_pass_id>/',
        view_application,
        name='view_application'
    ),

    path(
        'approve-application/<int:bus_pass_id>/',
        approve_application,
        name='approve_application'
    ),

    path(
        'reject-application/<int:bus_pass_id>/',
        reject_application,
        name='reject_application'
    ),
]