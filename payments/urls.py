# payments/urls.py

from django.urls import path

from .views import (
    payment_index,
    stripe_config,
    create_checkout_session,
    success,
    cancelled,
)

app_name = 'payments'

urlpatterns = [
    path('payments/index', payment_index, name='index'),
    path('payments/config', stripe_config),
    path('payments/create-checkout-session', create_checkout_session),
    path('payments/indexsuccess', success),
    path('payments/indexcancelled', cancelled),
]