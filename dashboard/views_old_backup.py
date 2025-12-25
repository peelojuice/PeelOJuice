from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta

from .decorators import superuser_required
from products.models import Juice, Category, Branch, BranchProduct
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


@superuser_required
def product_list(request):
    """List all products with search, branch and category filter"""
    
    products = Juice.objects.select_related('category').all()
    
    # Get all branches
    branches = Branch.objects.filter(is_active=True).order_by('city', 'name')
    
    # Filter by branch - default to first branch
    branch_id = request.GET.get('branch', '')
    if not branch_id and branches.exists():
        branch_id = str(branches.first().id)
    
    selected_branch = None
    if branch_id:
        try:
            selected_branch = Branch.objects.get(id=branch_id)
            # Filter products available at this branch
            available_product_ids = selected_branch.branch_products.filter(
                is_available=True
            ).values_list('product_id', flat=True)
            products = products.filter(id__in=available_product_ids)
        except Branch.DoesNotExist:
            pass
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by category
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Filter by status
    status = request.GET.get('status', '')
    if status == 'active':
        products = products.filter(is_active=True)
    elif status == 'inactive':
        products = products.filter(is_active=False)
    
    # Pagination
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Add branch availability status to each product
    if selected_branch:
        for product in page_obj:
            branch_product = BranchProduct.objects.filter(
                branch=selected_branch,
                product=product
            ).first()
            product.branch_available = branch_product.is_available if branch_product else False
    
    # Get all categories for filter dropdown
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'branches': branches,
        'selected_branch': selected_branch,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_status': status,
    }
    
    return render(request, 'dashboard/products/list.html', context)


@superuser_required
def product_add(request):
    """Add new product"""
    
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        long_description = request.POST.get('long_description', '')
        price = request.POST.get('price')
        net_quantity_ml = request.POST.get('net_quantity_ml', 300)
        ingredients = request.POST.get('ingredients')
        allergen_info = request.POST.get('allergen_info', 'Check with staff')
        is_active = request.POST.get('is_active') == 'on'
        
        # Process features (from textarea, one per line)
        features_text = request.POST.get('features', '')
        features = [f.strip() for f in features_text.split('\n') if f.strip()]
        
        # Process benefits (from textarea, one per line)
        benefits_text = request.POST.get('benefits', '')
        benefits_list = [{'title': b.strip(), 'description': b.strip()} for b in benefits_text.split('\n') if b.strip()]
        
        # Nutrition
        nutrition_calories = request.POST.get('nutrition_calories', 150)
        nutrition_total_fat = request.POST.get('nutrition_total_fat', 2.0)
        nutrition_carbohydrate = request.POST.get('nutrition_carbohydrate', 30.0)
        nutrition_dietary_fiber = request.POST.get('nutrition_dietary_fiber', 2.0)
        nutrition_total_sugars = request.POST.get('nutrition_total_sugars', 20.0)
        nutrition_protein = request.POST.get('nutrition_protein', 3.0)
        
        try:
            category = Category.objects.get(id=category_id)
            product = Juice.objects.create(
                name=name,
                category=category,
                description=description,
                long_description=long_description or description,
                price=price,
                net_quantity_ml=net_quantity_ml,
                ingredients=ingredients,
                is_active=is_active,
                features=features,
                benefits=benefits_list,
                allergen_info=allergen_info,
                nutrition_calories=nutrition_calories,
                nutrition_total_fat=nutrition_total_fat,
                nutrition_carbohydrate=nutrition_carbohydrate,
                nutrition_dietary_fiber=nutrition_dietary_fiber,
                nutrition_total_sugars=nutrition_total_sugars,
                nutrition_protein=nutrition_protein,
            )
            
            # Handle image upload
            if request.FILES.get('image'):
                product.image = request.FILES['image']
                product.save()
            
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('dashboard_products')
        except Exception as e:
            messages.error(request, f'Error creating product: {str(e)}')
    
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'dashboard/products/form.html', context)


@superuser_required
def product_edit(request, pk):
    """Edit product"""
    product = get_object_or_404(Juice, pk=pk)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.category_id = request.POST.get('category')
        product.description = request.POST.get('description')
        product.long_description = request.POST.get('long_description', '')
        product.price = request.POST.get('price')
        product.net_quantity_ml = request.POST.get('net_quantity_ml', 300)
        product.ingredients = request.POST.get('ingredients')
        product.allergen_info = request.POST.get('allergen_info', 'Check with staff')
        product.is_active = request.POST.get('is_active') == 'on'
        
        # Process features
        features_text = request.POST.get('features', '')
        product.features = [f.strip() for f in features_text.split('\n') if f.strip()]
        
        # Process benefits
        benefits_text = request.POST.get('benefits', '')
        product.benefits = [{'title': b.strip(), 'description': b.strip()} for b in benefits_text.split('\n') if b.strip()]
        
        # Nutrition
        product.nutrition_calories = request.POST.get('nutrition_calories', 150)
        product.nutrition_total_fat = request.POST.get('nutrition_total_fat', 2.0)
        product.nutrition_carbohydrate = request.POST.get('nutrition_carbohydrate', 30.0)
        product.nutrition_dietary_fiber = request.POST.get('nutrition_dietary_fiber', 2.0)
        product.nutrition_total_sugars = request.POST.get('nutrition_total_sugars', 20.0)
        product.nutrition_protein = request.POST.get('nutrition_protein', 3.0)
        
        # Handle image upload
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        
        try:
            product.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('dashboard_products')
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')
    
    categories = Category.objects.all()
    context = {'product': product, 'categories': categories}
    return render(request, 'dashboard/products/form.html', context)


@superuser_required
def product_toggle_status(request, pk):
    """Toggle product active status"""
    product = get_object_or_404(Juice, pk=pk)
    product.is_active = not product.is_active
    product.save()
    
    status = "activated" if product.is_active else "deactivated"
    messages.success(request, f'Product "{product.name}" {status} successfully!')
    return redirect('dashboard_products')


@superuser_required
def product_delete(request, pk):
    """Delete product"""
    product = get_object_or_404(Juice, pk=pk)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('dashboard_products')
    
    return render(request, 'dashboard/products/delete.html', {'product': product})


@superuser_required
def toggle_branch_availability(request, product_id, branch_id):
    """Toggle product availability for a specific branch"""
    
    try:
        branch = Branch.objects.get(id=branch_id)
        product = Juice.objects.get(id=product_id)
        
        # Get or create BranchProduct
        branch_product, created = BranchProduct.objects.get_or_create(
            branch=branch,
            product=product,
            defaults={'is_available': True}
        )
        
        # Toggle availability
        if not created:
            branch_product.is_available = not branch_product.is_available
            branch_product.save()
        
        return JsonResponse({
            'success': True,
            'is_available': branch_product.is_available
        })
    except (Branch.DoesNotExist, Juice.DoesNotExist):
        return JsonResponse({
            'success': False,
            'error': 'Branch or product not found'
        }, status=404)


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
def payment_list(request):
    """List all payments"""
    from payments.models import Payment
    from django.db.models import Sum
    
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
    from payments.models import Payment
    
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


@superuser_required
def user_list(request):
    """List all users"""
    
    users = User.objects.all().order_by('-created_at')
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(email__icontains=search_query) |
            Q(full_name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
    }
    
    return render(request, 'dashboard/users/list.html', context)
