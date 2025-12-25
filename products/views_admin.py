from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Juice
from .serializers import JuiceSerializer


class ToggleJuiceAvailabilityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admin users can toggle juice availability"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            juice = Juice.objects.get(pk=pk)
        except Juice.DoesNotExist:
            return Response(
                {"detail": "Juice not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        juice.is_available = not juice.is_available
        juice.save()

        return Response(
            {
                "message": "Juice availability toggled successfully",
                "juice_id": juice.id,
                "is_available": juice.is_available
            },
            status=status.HTTP_200_OK
        )


class ToggleJuiceActiveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admin users can toggle juice active status"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            juice = Juice.objects.get(pk=pk)
        except Juice.DoesNotExist:
            return Response(
                {"detail": "Juice not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        juice.is_active = not juice.is_active
        juice.save()

        return Response(
            {
                "message": "Juice active status toggled successfully",
                "juice_id": juice.id,
                "is_active": juice.is_active
            },
            status=status.HTTP_200_OK
        )


class UpdateJuicePriceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admin users can update juice price"},
                status=status.HTTP_403_FORBIDDEN
            )

        new_price = request.data.get('price')

        if not new_price:
            return Response(
                {"detail": "Price is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            new_price = float(new_price)
            if new_price < 0:
                raise ValueError
        except (ValueError, TypeError):
            return Response(
                {"detail": "Invalid price value"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            juice = Juice.objects.get(pk=pk)
        except Juice.DoesNotExist:
            return Response(
                {"detail": "Juice not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        juice.price = new_price
        juice.save()

        return Response(
            {
                "message": "Juice price updated successfully",
                "juice_id": juice.id,
                "price": str(juice.price)
            },
            status=status.HTTP_200_OK
        )
