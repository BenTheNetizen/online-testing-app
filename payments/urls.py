# payments/urls.py

from django.urls import path

from .views import (
    payment_index,
    stripe_config,
    create_checkout_session,
    success,
    cancelled,
    stripe_webhook
)

app_name = 'payments'

urlpatterns = [
    path('payments/index', payment_index, name='index'),
    path('payments/config', stripe_config, name='config'),
    path('payments/create-checkout-session', create_checkout_session, name='create-checkout-session'),
    path('payments/success/', success), # new
    path('payments/cancelled/', cancelled), # new
    path('payments/webhook/', stripe_webhook),
]