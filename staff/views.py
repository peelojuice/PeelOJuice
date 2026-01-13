from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import timedelta

# REST Framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from products.models import BranchProduct, Juice
from products.serializers import JuiceSerializer
from .decorators import staff_required, get_staff_branch_orders


def staff_login_view(request):
    """Staff login page"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('staff_dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_staff:
                if user.assigned_branch:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.get_full_name()}!')
                    return redirect('staff_dashboard')
                else:
                    messages.error(request, 'No branch assigned. Please contact administrator.')
            else:
                messages.error(request, 'You do not have staff access.')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'staff/login.html')


def staff_logout_view(request):
    """Staff logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('staff_login')


@staff_required
def staff_dashboard(request):
    """Staff dashboard home - shows overview of orders for assigned branch"""
    user = request.user
    branch = user.assigned_branch
    
    # Get all orders for this branch
    all_orders = get_staff_branch_orders(user)
    
    # Today's orders
    today = timezone.now().date()
    today_orders = all_orders.filter(created_at__date=today)
    
    # Order statistics
    stats = {
        'total_orders': all_orders.count(),
        'today_orders': today_orders.count(),
        'pending_orders': all_orders.filter(status='pending').count(),
        'preparing_orders': all_orders.filter(status='preparing').count(),
        'out_for_delivery': all_orders.filter(status='out_for_delivery').count(),
        'delivered_today': today_orders.filter(status='delivered').count(),
    }
    
    # Recent orders (last 10)
    recent_orders = all_orders[:10]
    
    context = {
        'branch': branch,
        'stats': stats,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'staff/dashboard.html', context)


@staff_required
def staff_orders_list(request):
    """List all orders for staff's assigned branch with filtering"""
    user = request.user
    branch = user.assigned_branch
    
    # Get all branch orders
    all_orders = get_staff_branch_orders(user)
    
    # Tab filter: 'active' or 'completed'
    tab = request.GET.get('tab', 'active')
    
    # Active orders: pending, confirmed, preparing
    active_orders = all_orders.filter(status__in=['pending', 'confirmed', 'preparing'])
    
    # Completed orders: out_for_delivery, delivered
    completed_orders = all_orders.filter(status__in=['out_for_delivery', 'delivered'])
    
    # Select orders based on tab
    if tab == 'completed':
        orders = completed_orders
    else:
        orders = active_orders
    
    # Status filter (within selected tab)
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Search by order number or customer
    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(
            Q(order_number__icontains=search_query) |
            Q(user__full_name__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
    
    context = {
        'branch': branch,
        'orders': orders,
        'tab': tab,
        'active_count': active_orders.count(),
        'completed_count': completed_orders.count(),
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': Order.STATUS_CHOICES,
    }
    
    return render(request, 'staff/orders_list.html', context)


@staff_required
def staff_order_detail(request, pk):
    """View and update specific order status"""
    user = request.user
    branch = user.assigned_branch
    
    # Get order for this branch only
    orders = get_staff_branch_orders(user)
    order = get_object_or_404(orders, pk=pk)
    
    # Staff can only update to these statuses (not delivered or cancelled)
    ALLOWED_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
    ]
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        
        # Validate status is in allowed list
        allowed_statuses = [choice[0] for choice in ALLOWED_STATUS_CHOICES]
        if new_status not in allowed_statuses:
            messages.error(request, 'Invalid status. Staff can only set: Pending, Confirmed, Preparing, or Out for Delivery.')
            return redirect('staff_order_detail', pk=pk)
        
        # Don't allow changes to delivered orders
        if order.status == 'delivered':
            messages.error(request, 'Cannot modify delivered orders.')
            return redirect('staff_order_detail', pk=pk)
        
        # Don't allow changes to cancelled orders
        if order.status == 'cancelled':
            messages.error(request, 'Cannot modify cancelled orders.')
            return redirect('staff_order_detail', pk=pk)
        
        order.status = new_status
        order.save()
        messages.success(request, f'Order status updated to {order.get_status_display()}')
        return redirect('staff_order_detail', pk=pk)
    
    context = {
        'order': order,
        'branch': branch,
        'status_choices': ALLOWED_STATUS_CHOICES,  # Only pass allowed statuses
    }
    
    return render(request, 'staff/order_detail.html', context)


# ========== REST API ENDPOINTS FOR MOBILE APP ==========

class StaffBranchProductsAPIView(APIView):
    """API endpoint to get all products for staff's branch with availability status"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Verify user is staff
        if not request.user.is_staff:
            return Response(
                {'error': 'Only staff members can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Verify staff has assigned branch
        if not request.user.assigned_branch:
            return Response(
                {'error': 'No branch assigned to this staff member'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        branch = request.user.assigned_branch
        
        # Get all branch products for this branch
        branch_products = BranchProduct.objects.filter(
            branch=branch
        ).select_related('product', 'product__category').order_by(
            'product__category__name', 'product__name'
        )
        
        # Format response with product details and availability
        products_data = []
        for bp in branch_products:
            product = bp.product
            products_data.append({
                'branch_product_id': bp.id,
                'product_id': product.id,
                'name': product.name,
                'description': product.description,
                'price': str(product.price),
                'image': f"https://res.cloudinary.com/dxizjczfh/image/upload/{str(product.image).replace('media/', '', 1)}" if product.image else None,
                'category': {
                    'id': product.category.id,
                    'name': product.category.name
                } if product.category else None,
                'is_available': bp.is_available,
                'is_active': product.is_active,
                'updated_at': bp.updated_at
            })
        
        return Response({
            'branch': {
                'id': branch.id,
                'name': branch.name,
                'city': branch.city
            },
            'products': products_data,
            'total_products': len(products_data),
            'available_products': sum(1 for p in products_data if p['is_available'])
        }, status=status.HTTP_200_OK)


class ToggleBranchProductAvailabilityAPIView(APIView):
    """API endpoint to toggle product availability at staff's branch"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, branch_product_id):
        # Verify user is staff
        if not request.user.is_staff:
            return Response(
                {'error': 'Only staff members can toggle product availability'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Verify staff has assigned branch
        if not request.user.assigned_branch:
            return Response(
                {'error': 'No branch assigned to this staff member'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        branch = request.user.assigned_branch
        
        # Get the branch product (ensure it belongs to staff's branch)
        try:
            branch_product = BranchProduct.objects.select_related('product').get(
                id=branch_product_id,
                branch=branch
            )
        except BranchProduct.DoesNotExist:
            return Response(
                {'error': 'Product not found in your branch inventory'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Toggle availability
        branch_product.is_available = not branch_product.is_available
        branch_product.save()
        
        return Response({
            'message': f"Product availability updated successfully",
            'branch_product_id': branch_product.id,
            'product_name': branch_product.product.name,
            'is_available': branch_product.is_available,
            'updated_at': branch_product.updated_at
        }, status=status.HTTP_200_OK)
