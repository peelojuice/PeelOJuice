from django.urls import path
from .views import (
    ConfirmCODPaymentAPIView, 
    GetPaymentDetailsAPIView,
    CreateRazorpayOrderAPIView,
    VerifyRazorpayPaymentAPIView,
    RazorpayWebhookAPIView
)

urlpatterns = [
    path('cod/<int:pk>/confirm/', ConfirmCODPaymentAPIView.as_view(), name='confirm-cod-payment'),
    path('order/<int:order_id>/', GetPaymentDetailsAPIView.as_view(), name='get-payment-details'),
    path('razorpay/create-order/', CreateRazorpayOrderAPIView.as_view(), name='create-razorpay-order'),
    path('razorpay/verify/', VerifyRazorpayPaymentAPIView.as_view(), name='verify-razorpay-payment'),
    path('razorpay/webhook/', RazorpayWebhookAPIView.as_view(), name='razorpay-webhook'),
]
