from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

from dashboard.decorators import superuser_required
from products.models import Juice, Category
from orders.models import Order
from users.models import User


@superuser_required
def dashboard_home(request):
    """Admin dashboard homepage with stats and analytics"""
    
    # Calculate statistics
    total_products = Juice.objects.count()
    active_products = Juice.objects.filter(is_active=True).count()
    total_categories = Category.objects.count()
    total_users = User.objects.count()
    
    # Order statistics
    total_orders = Order.objects.count()
    today = timezone.now().date()
    orders_today = Order.objects.filter(created_at__date=today).count()
    orders_this_week = Order.objects.filter(
        created_at__gte=today - timedelta(days=7)
    ).count()
    
    # Revenue
    total_revenue = Order.objects.filter(
        status__in=['delivered', 'confirmed']
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Recent orders and products
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
    popular_products = Juice.objects.filter(is_active=True).order_by('-id')[:10]
    low_stock_products = []
    
    context = {
        'total_products': total_products,
        'active_products': active_products,
        'total_categories': total_categories,
        'total_users': total_users,
        'total_orders': total_orders,
        'orders_today': orders_today,
        'orders_this_week': orders_this_week,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'popular_products': popular_products,
        'low_stock_products': low_stock_products,
    }
    
    return render(request, 'dashboard/index.html', context)
