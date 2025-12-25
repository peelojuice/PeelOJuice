from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied
from .models import User

class EmailPhoneAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if not user.check_password(password):
            return None

        if not user.is_email_verified:
            raise PermissionDenied("Email is not verified")

        if not user.is_phone_verified:
            raise PermissionDenied("Phone number is not verified")

        return user
