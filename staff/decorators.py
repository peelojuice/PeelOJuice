from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden


def staff_required(view_func):
    """
    Decorator for views that checks that the user is authenticated,
    is staff, and has an assigned branch.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('staff_login')
        
        if not request.user.is_staff:
            return HttpResponseForbidden("Staff access only. Please contact administrator.")
        
        if not request.user.assigned_branch:
            return HttpResponseForbidden("No branch assigned. Please contact administrator.")
        
        return view_func(request, *args, **kwargs)
    return wrapper


def get_staff_branch_orders(user):
    """
    Helper function to get orders filtered by staff's assigned branch.
    Returns empty queryset if user has no assigned branch.
    """
    from orders.models import Order
    
    if not user.assigned_branch:
        return Order.objects.none()
    
    return Order.objects.filter(branch=user.assigned_branch).select_related(
        'user', 'branch'
    ).prefetch_related('items__juice').order_by('-created_at')
