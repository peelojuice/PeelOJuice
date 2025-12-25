from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Coupon
from .serializers import CouponSerializer, ValidateCouponSerializer
from decimal import Decimal


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_coupon(request):
    """Validate a coupon code and return discount information"""
    serializer = ValidateCouponSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    code = serializer.validated_data['code'].upper()
    cart_total = serializer.validated_data.get('cart_total', Decimal('0.00'))
    
    try:
        coupon = Coupon.objects.get(code=code)
    except Coupon.DoesNotExist:
        return Response(
            {'error': 'Invalid coupon code'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Validate coupon
    is_valid, message = coupon.is_valid()
    if not is_valid:
        return Response(
            {'error': message},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check minimum order value
    if cart_total < coupon.min_order_value:
        return Response(
            {'error': f'Minimum order value of ₹{coupon.min_order_value} required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Calculate discount
    discount_amount = coupon.calculate_discount(cart_total)
    
    return Response({
        'coupon': CouponSerializer(coupon).data,
        'discount_amount': float(discount_amount),
        'message': f'Coupon applied! You saved ₹{discount_amount}'
    })
