from django.urls import path
from .views import *
from .views_verify import *
from .views_admin import (
    ToggleUserActiveAPIView,
    VerifyUserEmailAPIView,
    VerifyUserPhoneAPIView,
    ResetUserOTPLockAPIView
)
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Traditional Django Authentication (for server-side login)
    path('web/login/', CustomLoginView.as_view(), name='web_login'),
    path('web/logout/', LogoutView.as_view(next_page='web_login'), name='web_logout'),
    
    # API Endpoints
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('fcm-token/', UpdateFCMTokenAPIView.as_view(), name='fcm-token'),
    
    path('verify-email/', VerifyEmailOTPAPIView.as_view(), name='verify-email'),
    path('verify-phone/', VerifyPhoneOTPAPIView.as_view(), name='verify-phone'),
    
    path('resend-email-otp/', ResendEmailOTPAPIView.as_view(), name='resend-email-otp'),
    path('resend-phone-otp/', ResendPhoneOTPAPIView.as_view(), name='resend-phone-otp'),
    
    path('password-reset/request/', RequestPasswordResetOTPAPIView.as_view(), name='request-password-reset'),
    path('password-reset/verify/', VerifyPasswordResetOTPAPIView.as_view(), name='verify-password-reset-otp'),
    path('password-reset/confirm/', ConfirmPasswordResetAPIView.as_view(), name='confirm-password-reset'),
    
    path('admin/users/<int:pk>/toggle-active/', ToggleUserActiveAPIView.as_view(), name='toggle-user-active'),
    path('admin/users/<int:pk>/verify-email/', VerifyUserEmailAPIView.as_view(), name='admin-verify-email'),
    path('admin/users/<int:pk>/verify-phone/', VerifyUserPhoneAPIView.as_view(), name='admin-verify-phone'),
    path('admin/users/<int:pk>/reset-otp-lock/', ResetUserOTPLockAPIView.as_view(), name='reset-otp-lock'),
]
