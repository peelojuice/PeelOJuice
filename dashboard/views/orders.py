from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

from dashboard.decorators import superuser_required
from orders.models import Order


@superuser_required
def order_list(request):
    """List all orders"""
    
    orders = Order.objects.select_related('user').prefetch_related('payment').order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Filter by payment status
    payment_status_filter = request.GET.get('payment_status', '')
    if payment_status_filter:
        orders = orders.filter(payment__status=payment_status_filter)
    
    # Pagination
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'selected_status': status_filter,
        'selected_payment_status': payment_status_filter,
    }
    
    return render(request, 'dashboard/orders/list.html', context)


@superuser_required
def order_update_status(request, order_id):
    """Update order status with business rules"""
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        
        if new_status not in dict(Order.STATUS_CHOICES):
            messages.error(request, 'Invalid order status')
            return redirect('dashboard_orders')
        
        # Business Rule 3: Delivered orders cannot be changed
        if order.status == 'delivered':
            messages.error(request, f'Order #{order.id} has already been delivered and cannot be modified')
            return redirect('dashboard_orders')
        
        # Business Rule 1: To mark as delivered, payment must be completed
        if new_status == 'delivered':
            if not hasattr(order, 'payment') or order.payment.status != 'completed':
                messages.error(request, f'Cannot mark Order #{order.id} as delivered. Payment must be completed first!')
                return redirect('dashboard_orders')
        
        # Business Rule 2: If cancelling order, refund the payment
        if new_status == 'cancelled':
            if hasattr(order, 'payment') and order.payment.status == 'completed':
                order.payment.status = 'refunded'
                order.payment.save()
                messages.info(request, f'Payment #{order.payment.id} automatically refunded due to order cancellation')
        
        order.status = new_status
        order.save()
        messages.success(request, f'Order #{order.id} status updated to {order.get_status_display()}')
    
    return redirect('dashboard_orders')
