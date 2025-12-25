from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Address
from .serializers import AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user addresses
    - List: GET /api/addresses/
    - Create: POST /api/addresses/
    - Retrieve: GET /api/addresses/{id}/
    - Update: PUT /api/addresses/{id}/
    - Delete: DELETE /api/addresses/{id}/
    - Set Default: POST /api/addresses/{id}/set_default/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        # Only return addresses belonging to the current user
        return Address.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """Set an address as default"""
        address = self.get_object()
        
        # Unset all other defaults for this user
        Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
        
        # Set this address as default
        address.is_default = True
        address.save()
        
        return Response({
            'message': 'Address set as default',
            'address': AddressSerializer(address).data
        })
