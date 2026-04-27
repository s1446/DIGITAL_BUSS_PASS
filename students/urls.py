from django.urls import path
from .views import (
    apply_bus_pass,
    check_status,
    request_renewal,
    select_pass_type,
    government_employee_apply,
    non_government_employee_apply,
    citizen_apply,
    pwd_apply
)

urlpatterns = [
    path('apply-pass/', apply_bus_pass, name='apply_bus_pass'),
    path('status/', check_status, name='check_status'),
    path('renew-pass/', request_renewal, name='request_renewal'),
    path('select-pass-type/', select_pass_type, name='select_pass_type'),
    path( 'government-employee-form/',government_employee_apply,name='government_employee_apply'),
    path('non-government-employee-form/',non_government_employee_apply,name='non_government_employee_apply'),
    path('citizen-form/',citizen_apply,name='citizen_apply'),
    path('pwd-form/', pwd_apply,name='pwd_apply'),

]