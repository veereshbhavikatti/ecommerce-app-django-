from django.urls import path
from .views import PaymentInitView, PaymentVerifyView

urlpatterns = [
    path('init/', PaymentInitView.as_view(), name='payment-init'),
    path('verify/', PaymentVerifyView.as_view(), name='payment-verify'),
]
