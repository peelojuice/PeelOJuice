from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from .models import User

def is_otp_expired(user, expiry_minutes=5, otp_type='email'):
    if otp_type == 'phone':
        otp_created_field = user.phone_otp_created_at
    elif otp_type == 'password_reset':
        otp_created_field = user.password_reset_otp_created_at
    else:
        otp_created_field = user.otp_created_at

    if not otp_created_field:
        return True

    return timezone.now() - otp_created_field > timedelta(minutes=expiry_minutes)

def is_otp_locked(user):
    if user.otp_locked_until and timezone.now() < user.otp_locked_until:
        reset_otp_attempts(user)
        return True
    return False


def lock_otp(user, minutes=15):
    user.otp_locked_until = timezone.now() + timedelta(minutes=minutes)
    user.save(update_fields=['otp_locked_until'])


def reset_otp_attempts(user):
    user.otp_failed_attempts = 0
    user.otp_locked_until = None
    user.save(update_fields=['otp_failed_attempts', 'otp_locked_until'])

class VerifyEmailOTPAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response(
                {
                    "message" : "Email and OTP are required"
                },
                status= status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {
                    "message" : "User Not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if is_otp_locked(user):
            return Response(
                {"message": "OTP temporarily locked. Try again later."},
                status=status.HTTP_423_LOCKED
            )
        
        if user.email_otp != otp:
            user.otp_failed_attempts += 1

            if user.otp_failed_attempts >= 5:
                lock_otp(user)
                return Response(
                    {"message": "Too many wrong attempts. OTP locked for 15 minutes."},
                    status=status.HTTP_423_LOCKED
                )

            user.save(update_fields=['otp_failed_attempts'])

            return Response(
                {"message": "Invalid OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if is_otp_expired(user):
            return Response(
                {
                    "message" : "OTP Expired"
                },
                status=status.HTTP_408_REQUEST_TIMEOUT
            )
        
        reset_otp_attempts(user)
        user.is_email_verified = True
        user.email_otp = None
        user.otp_created_at = None
        user.save(update_fields=[
            'is_email_verified',
            'email_otp',
            'otp_created_at'
        ])
        
        return Response(
            {
                "message" : "Email is Verified Successfully"
            },
            status=status.HTTP_200_OK
        )
    

class VerifyPhoneOTPAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        if not phone_number or not otp:
            return Response(
                {"message": "Phone number and OTP are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if is_otp_locked(user):
            return Response(
                {"message": "OTP temporarily locked. Try again later."},
                status=status.HTTP_423_LOCKED
            )

        if user.phone_otp != otp:
            user.otp_failed_attempts += 1

            if user.otp_failed_attempts >= 5:
                lock_otp(user)
                return Response(
                    {"message": "Too many wrong attempts. OTP locked for 15 minutes."},
                    status=status.HTTP_423_LOCKED
                )

            user.save(update_fields=['otp_failed_attempts'])

            return Response(
                {"message": "Invalid OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if is_otp_expired(user, otp_type='phone'):
            return Response(
                {"message": "OTP expired"},
                status=status.HTTP_408_REQUEST_TIMEOUT
            )

        reset_otp_attempts(user)
        user.is_phone_verified = True
        user.phone_otp = None
        user.phone_otp_created_at = None

        user.save(update_fields=[
            'is_phone_verified',
            'phone_otp',
            'phone_otp_created_at'
        ])

        return Response(
            {"message": "Phone number verified successfully"},
            status=status.HTTP_200_OK
        )

class VerifyPasswordResetOTPAPIView(APIView):
    
    def post(self, request):
        email_or_phone = request.data.get('email_or_phone')
        otp = request.data.get('otp')
        
        if not email_or_phone or not otp:
            return Response(
                {"message": "Email/phone and OTP are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            try:
                user = User.objects.get(email=email_or_phone)
            except User.DoesNotExist:
                user = User.objects.get(phone_number=email_or_phone)
        except User.DoesNotExist:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if is_otp_locked(user):
            return Response(
                {"message": "OTP temporarily locked. Try again later."},
                status=status.HTTP_423_LOCKED
            )
        
        if user.password_reset_otp != otp:
            user.otp_failed_attempts += 1

            if user.otp_failed_attempts >= 5:
                lock_otp(user)
                return Response(
                    {"message": "Too many wrong attempts. OTP locked for 15 minutes."},
                    status=status.HTTP_423_LOCKED
                )

            user.save(update_fields=['otp_failed_attempts'])

            return Response(
                {"message": "Invalid OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user.password_reset_otp_verified:
            return Response(
                {"message": "OTP already used"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if is_otp_expired(user, otp_type='password_reset'):
            return Response(
                {"message": "OTP expired"},
                status=status.HTTP_408_REQUEST_TIMEOUT
            )

        reset_otp_attempts(user)
        user.password_reset_otp_verified = True
        user.password_reset_otp = None
        user.save(update_fields=['password_reset_otp_verified', 'password_reset_otp'])
        
        return Response(
            {"message": "OTP verified"},
            status=status.HTTP_200_OK
        )