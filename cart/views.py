from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartSerializer
from .utils import get_or_create_cart
from products.models import Juice
from coupons.models import Coupon

class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        juice_id = request.data.get('juice_id')
        quantity = int(request.data.get('quantity', 1))

        if quantity < 1:
            return Response(
                {"message": "Quantity must be at least 1"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            juice = Juice.objects.get(id=juice_id, is_active=True)
        except Juice.DoesNotExist:
            return Response(
                {"message": "Juice not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cart = get_or_create_cart(request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            juice=juice,
            defaults={
                'quantity': quantity,
                'price_at_added': juice.price
            }
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ViewCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class UpdateCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        juice_id = request.data.get('juice_id')
        action = request.data.get('action')

        if not juice_id or action not in ['increment', 'decrement']:
            return Response(
                {"message": "Invalid request. Provide juice_id and action (increment/decrement)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if not cart:
            return Response(
                {"message": "Cart not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            item = CartItem.objects.get(cart=cart, juice_id=juice_id)
        except CartItem.DoesNotExist:
            return Response(
                {"message": "Item not in cart"},
                status=status.HTTP_404_NOT_FOUND
            )

        if action == 'increment':
            item.quantity += 1
            item.save()

        elif action == 'decrement':
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
                return Response(
                    {"message": "Item removed from cart"},
                    status=status.HTTP_200_OK
                )

        return Response(
            {
                "message": "Cart updated successfully",
                "item_quantity": item.quantity
            },
            status=status.HTTP_200_OK
        )

class RemoveCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        juice_id = request.data.get('juice_id')

        if not juice_id:
            return Response(
                {"message": "Juice ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if not cart:
            return Response(
                {"message": "Cart not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        deleted, _ = CartItem.objects.filter(
            cart=cart,
            juice_id=juice_id
        ).delete()

        if not deleted:
            return Response(
                {"message": "Item not found in cart"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"message": "Item removed successfully"},
            status=status.HTTP_200_OK
        )

class ApplyCouponAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        code = request.data.get('code', '').upper()
        
        if not code:
            return Response(
                {"error": "Coupon code is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart = get_or_create_cart(request.user)
        
        # Check if coupon exists
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return Response(
                {"error": "Invalid coupon code"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Validate coupon
        is_valid, message = coupon.is_valid()
        if not is_valid:
            return Response(
                {"error": message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check minimum order value
        if cart.total_amount < coupon.min_order_value:
            return Response(
                {"error": f"Minimum order value of ₹{coupon.min_order_value} required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Apply coupon to cart
        cart.applied_coupon = coupon
        cart.save()
        
        # Calculate discount
        discount = coupon.calculate_discount(cart.total_amount)
        
        serializer = CartSerializer(cart)
        return Response({
            "message": f"Coupon applied! You saved ₹{discount}",
            "cart": serializer.data
        }, status=status.HTTP_200_OK)

class RemoveCouponAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        cart = get_or_create_cart(request.user)
        
        if not cart.applied_coupon:
            return Response(
                {"error": "No coupon applied"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart.applied_coupon = None
        cart.save()
        
        serializer = CartSerializer(cart)
        return Response({
            "message": "Coupon removed successfully",
            "cart": serializer.data
        }, status=status.HTTP_200_OK)

class UpdateItemInstructionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        juice_id = request.data.get('juice_id')
        instructions = request.data.get('instructions', '')

        if not juice_id:
            return Response(
                {"message": "Juice ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if not cart:
            return Response(
                {"message": "Cart not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            item = CartItem.objects.get(cart=cart, juice_id=juice_id)
            # Truncate if too long (backup check)
            if len(instructions) > 200:
                instructions = instructions[:200]
            
            item.cooking_instructions = instructions
            item.save()
            
            return Response(
                {
                    "message": "Instructions updated",
                    "instructions": item.cooking_instructions
                },
                status=status.HTTP_200_OK
            )
        except CartItem.DoesNotExist:
            return Response(
                {"message": "Item not in cart"},
                status=status.HTTP_404_NOT_FOUND
            )
