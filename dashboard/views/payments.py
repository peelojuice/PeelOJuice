from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum

from dashboard.decorators import superuser_required
from payments.models import Payment


@superuser_required
def payment_list(request):
    """List all payments"""
    
    payments = Payment.objects.select_related('order', 'order__user').order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    # Filter by method
    method_filter = request.GET.get('method', '')
    if method_filter:
        payments = payments.filter(method=method_filter)
    
    # Calculate stats
    total_revenue = Payment.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    completed_count = Payment.objects.filter(status='completed').count()
    
    # Pagination
    paginator = Paginator(payments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'selected_status': status_filter,
        'selected_method': method_filter,
        'total_revenue': total_revenue,
        'completed_count': completed_count,
    }
    
    return render(request, 'dashboard/payments/list.html', context)


@superuser_required
def payment_update_status(request, payment_id):
    """Update payment status with business rules"""
    
    if request.method == 'POST':
        payment = get_object_or_404(Payment, id=payment_id)
        new_status = request.POST.get('status')
        
        if new_status not in dict(Payment.PAYMENT_STATUS):
            messages.error(request, 'Invalid payment status')
            return redirect('dashboard_payments')
        
        # Business Rule 3 (Extended): Cannot change payment for delivered orders
        if payment.order.status == 'delivered':
            messages.error(request, f'Cannot modify payment for Order #{payment.order.id}. Order has already been delivered!')
            return redirect('dashboard_payments')
        
        # Business Rule 2: If changing payment to refunded, order must be cancelled
        if new_status == 'refunded':
            if payment.order.status != 'cancelled':
                payment.order.status = 'cancelled'
                payment.order.save()
                messages.info(request, f'Order #{payment.order.id} automatically cancelled due to refund')
        
        payment.status = new_status
        payment.save()
        messages.success(request, f'Payment #{payment.id} status updated to {payment.get_status_display()}')
    
    return redirect('dashboard_payments')
