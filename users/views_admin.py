from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import User


class ToggleUserActiveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admin users can toggle user active status"},
                status=status.HTTP_403_FORBIDDEN
            )


        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        user.is_active = not user.is_active
        user.save()

        return Response(
            {
                "message": "User active status toggled successfully",
                "user_id": user.id,
                "is_active": user.is_active
            },
            status=status.HTTP_200_OK
        )


class VerifyUserEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admin users can verify user email"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if user.is_email_verified:
            return Response(
                {"detail": "Email is already verified"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_email_verified = True
        user.save()

        return Response(
            {
                "message": "User email verified successfully",
                "user_id": user.id
            },
            status=status.HTTP_200_OK
        )


class VerifyUserPhoneAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admin users can verify user phone"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if user.is_phone_verified:
            return Response(
                {"detail": "Phone is already verified"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_phone_verified = True
        user.save()

        return Response(
            {
                "message": "User phone verified successfully",
                "user_id": user.id
            },
            status=status.HTTP_200_OK
        )


class ResetUserOTPLockAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admin users can reset OTP lock"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        user.otp_failed_attempts = 0
        user.otp_locked_until = None
        user.save()

        return Response(
            {
                "message": "OTP lock reset successfully",
                "user_id": user.id
            },
            status=status.HTTP_200_OK
        )
