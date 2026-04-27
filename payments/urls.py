# payments/urls.py

from django.urls import path
from .views import (
    payment_verification,
    select_plan,
    payment_gateway,
    final_pass,
)

urlpatterns = [
    path(
        'payment/',
        payment_verification,
        name='payment'
    ),

    path(
        'select-plan/',
        select_plan,
        name='select_plan'
    ),

    path(
        'payment-gateway/<str:plan_name>/<int:amount>/',
        payment_gateway,
        name='payment_gateway'
    ),

    path(
        'final-pass/',
        final_pass,
        name='final_pass'
    ),
]