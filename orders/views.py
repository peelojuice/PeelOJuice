from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction
from rest_framework.generics import RetrieveAPIView
from decimal import Decimal

from cart.models import Cart, CartItem
from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderListSerializer, OrderDetailSerializer
from .email_utils import send_order_confirmation_email

class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        from payments.models import Payment
        
        user = request.user
        payment_method = request.data.get('payment_method', 'cod')
        branch_id = request.data.get('branch_id')

        if payment_method not in ['cod', 'online']:
            return Response(
                {"detail": "Invalid payment method. Choose 'cod' or 'online'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate branch selection
        if not branch_id:
            return Response(
                {"detail": "Branch selection is required. Please select a branch before checkout."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response(
                {"detail": "Cart not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response(
                {"detail": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate subtotal using price_at_added (cart prices)
        food_subtotal = sum(
            item.price_at_added * item.quantity for item in cart_items
        )
        
        # Calculate coupon discount if applied
        discount = 0
        if cart.applied_coupon is not None:
            try:
                discount = cart.applied_coupon.calculate_discount(food_subtotal)
            except Exception as e:
                print(f"[ERROR] Coupon discount calculation failed: {str(e)}")
                discount = 0

        # Get the selected branch from request
        from products.models import Branch
        try:
            branch = Branch.objects.get(id=branch_id, is_active=True)
            print(f"[SUCCESS] Branch selected: ID={branch.id}, Name={branch.name}")
        except Branch.DoesNotExist:
            return Response(
                {"detail": "Selected branch not found or is inactive. Please select a valid branch."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(f"[ERROR] Branch fetch failed: {str(e)}")
            return Response(
                {"detail": f"Branch error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Calculate delivery fee (free if subtotal >= 99, otherwise 20)
        # This matches the cart serializer logic to ensure payment amount consistency
        delivery_fee_base = Decimal('0.00') if food_subtotal >= Decimal('99.00') else Decimal('20.00')

        # Create order
        try:
            order = Order.objects.create(
                user=user,
                branch=branch,
                food_subtotal=food_subtotal,
                delivery_fee_base=delivery_fee_base,
                platform_fee=10,
                discount=discount
            )
            print(f"[SUCCESS] Order created: ID={order.id}, Branch={branch.name}")
        except Exception as e:
            print(f"[ERROR] Order creation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response(
                {"detail": f"Order creation error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Create order items
        try:
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    juice=item.juice,
                    quantity=item.quantity,
                    price_per_item=item.price_at_added
                )
            print(f"[SUCCESS] Created {cart_items.count()} order items")
        except Exception as e:
            print(f"[ERROR] Order items creation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response(
                {"detail": f"Order items error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Calculate totals
        try:
            order.calculate_totals()
            order.save()
            print(f"[SUCCESS] Order totals calculated: Rs.{order.total_amount}")
        except Exception as e:
            print(f"[ERROR] Total calculation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response(
                {"detail": f"Total calculation error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Create payment
        try:
            Payment.objects.create(
                order=order,
                method=payment_method,
                amount=order.total_amount,
                status='pending'
            )
            print(f"[SUCCESS] Payment created: {payment_method}")
        except Exception as e:
            print(f"[ERROR] Payment creation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response(
                {"detail": f"Payment error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Clear cart only for COD orders
        # For online payments, cart will be cleared after successful payment verification
        if payment_method == 'cod':
            try:
                cart_items.delete()
                cart.applied_coupon = None
                cart.save()
                print(f"[SUCCESS] Cart cleared for COD order")
            except Exception as e:
                print(f"[WARNING] Cart clearing failed: {str(e)}")

        # Send order confirmation email (non-critical)
        try:
            email_sent = send_order_confirmation_email(order, user)
            if email_sent:
                print(f"[SUCCESS] Order confirmation email sent to {user.email}")
            else:
                print(f"[WARNING] Email sending returned False for order #{order.id}")
        except Exception as e:
            print(f"[WARNING] Email failed for order #{order.id}: {str(e)}")

        # Send push notifications to branch staff
        try:
            from users.fcm_service import send_new_order_notification
            from users.models import User
            
            # Get all active staff members assigned to this branch with FCM tokens
            branch_staff = User.objects.filter(
                assigned_branch=branch,
                is_staff=True,
                is_active=True,
                fcm_token__isnull=False  # Only staff with registered FCM tokens
            ).exclude(fcm_token='')
            
            # Send notification to each staff member
            notification_count = 0
            for staff_member in branch_staff:
                if send_new_order_notification(staff_member.fcm_token, order):
                    notification_count += 1
            
            if notification_count > 0:
                print(f"[SUCCESS] Sent notifications to {notification_count} staff members for order #{order.order_number}")
            else:
                print(f"[WARNING] No staff notifications sent for order #{order.order_number} (no staff with FCM tokens)")
                
        except Exception as e:
            # Don't fail the order if notification fails
            print(f"[ERROR] Failed to send notifications: {str(e)}")

        # Serialize and return
        try:
            serializer = OrderSerializer(order)
            return Response(
                {
                    "message": "Order placed successfully",
                    "order": serializer.data,
                    "payment_method": payment_method
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print(f"[ERROR] Serialization failed: {str(e)}")
            return Response(
                {"detail": f"Serialization error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class MyOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        status_filter = request.query_params.get('status')

        orders = Order.objects.filter(user=user).order_by('-created_at')

        if status_filter == 'ongoing':
            orders = orders.filter(
                status__in=[
                    'pending',
                    'confirmed',
                    'preparing',
                    'out_for_delivery'
                ]
            )

        elif status_filter == 'delivered':
            orders = orders.filter(status='delivered')

        elif status_filter == 'cancelled':
            orders = orders.filter(status='cancelled')

        serializer = MyOrderListSerializer(orders, many=True)

        return Response({
            "count": orders.count(),
            "orders": serializer.data
        })

class StaffOrdersAPIView(APIView):
    """
    REST API endpoint for staff to get orders assigned to their branch.
    Used by staff mobile app.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Check if user is staff
        if not user.is_staff:
            return Response(
                {"detail": "Only staff members can access this endpoint"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if staff has assigned branch
        if not user.assigned_branch:
            return Response(
                {"detail": "No branch assigned. Please contact administrator."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get status filter from query params
        status_filter = request.query_params.get('status')
        
        # Get orders for this staff member's assigned branch
        orders = Order.objects.filter(
            branch=user.assigned_branch
        ).order_by('-created_at')
        
        # Apply status filtering if provided
        if status_filter == 'ongoing':
            orders = orders.filter(
                status__in=[
                    'pending',
                    'confirmed',
                    'preparing',
                    'out_for_delivery'
                ]
            )
        elif status_filter == 'delivered':
            orders = orders.filter(status='delivered')
        elif status_filter == 'cancelled':
            orders = orders.filter(status='cancelled')
        elif status_filter:
            # If a specific status is provided
            orders = orders.filter(status=status_filter)
        
        serializer = MyOrderListSerializer(orders, many=True)
        
        return Response({
            "count": orders.count(),
            "orders": serializer.data,
            "branch": {
                "id": user.assigned_branch.id,
                "name": user.assigned_branch.name,
                "city": user.assigned_branch.city
            }
        })

class StaffOrderDetailAPIView(APIView):
    """
    REST API endpoint for staff to get a specific order detail.
    Only returns orders from the staff's assigned branch.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        user = request.user
        
        # Check if user is staff
        if not user.is_staff:
            return Response(
                {"detail": "Only staff members can access this endpoint"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if staff has assigned branch
        if not user.assigned_branch:
            return Response(
                {"detail": "No branch assigned. Please contact administrator."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get order from staff's branch only
        try:
            order = Order.objects.select_related(
                'user', 'branch'
            ).prefetch_related('items__juice').get(
                pk=pk,
                branch=user.assigned_branch
            )
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found or not assigned to your branch"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)

class OrderDetailAPIView(RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CancelOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user

        try:
            order = Order.objects.get(pk=pk, user=user)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validation: Check if order can be cancelled
        if order.status == 'delivered':
            return Response(
                {"detail": "Cannot cancel a delivered order"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if order.status == 'cancelled':
            return Response(
                {"detail": "Order is already cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = 'cancelled'
        order.save()

        return Response(
            {
                "message": "Order cancelled successfully",
                "order_id": order.id,
                "status": order.status
            },
            status=status.HTTP_200_OK
        )


class UpdateOrderStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user

        if not user.is_staff:
            return Response(
                {"detail": "Only admin users can update order status"},
                status=status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get('status')

        if not new_status:
            return Response(
                {"detail": "Status is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {"detail": f"Invalid status. Valid options: {', '.join(valid_statuses)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if order.status == 'cancelled':
            return Response(
                {"detail": "Cannot update status of a cancelled order"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if order.status == 'delivered' and new_status != 'delivered':
            return Response(
                {"detail": "Cannot change status of a delivered order"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        return Response(
            {
                "message": "Order status updated successfully",
                "order_id": order.id,
                "status": order.status
            },
            status=status.HTTP_200_OK
        )
