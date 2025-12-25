from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

from dashboard.decorators import superuser_required
from products.models import Juice, Category, Branch, BranchProduct


@superuser_required
def product_list(request):
    """List all products with filters and pagination"""
    
    products = Juice.objects.select_related('category').order_by('id')
    
    # Handle branch selection from GET parameter
    branch_param = request.GET.get('branch', '')
    if branch_param:
        try:
            branch_id = int(branch_param)
            selected_branch = Branch.objects.filter(id=branch_id, is_active=True).first()
            if selected_branch:
                request.session['selected_branch_id'] = selected_branch.id
                request.session.modified = True  # Explicitly mark session as modified
        except (ValueError, TypeError):
            pass
    
    # Get selected branch from session or first branch
    selected_branch_id = request.session.get('selected_branch_id')
    selected_branch = None
    
    if selected_branch_id:
        selected_branch = Branch.objects.filter(id=selected_branch_id).first()
    
    if not selected_branch:
        selected_branch = Branch.objects.filter(is_active=True).first()
        if selected_branch:
            request.session['selected_branch_id'] = selected_branch.id
            request.session.modified = True  # Explicitly mark session as modified
    
    # Category filter
    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    # Status filter
    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        products = products.filter(is_active=True)
    elif status_filter == 'inactive':
        products = products.filter(is_active=False)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Availability filter (filter by branch availability)
    availability_filter = request.GET.get('availability', '')
    if availability_filter and selected_branch:
        if availability_filter == 'available':
            # Get products that are available in the selected branch
            available_product_ids = BranchProduct.objects.filter(
                branch=selected_branch,
                is_available=True
            ).values_list('product_id', flat=True)
            products = products.filter(id__in=available_product_ids)
        elif availability_filter == 'not_available':
            # Get products that are not available or not in BranchProduct for this branch
            available_product_ids = BranchProduct.objects.filter(
                branch=selected_branch,
                is_available=True
            ).values_list('product_id', flat=True)
            products = products.exclude(id__in=available_product_ids)
    
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
    
    categories = Category.objects.all()
    branches = Branch.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'branches': branches,
        'selected_branch': selected_branch,
        'selected_category': category_filter,
        'selected_status': status_filter,
        'selected_availability': availability_filter,
        'search_query': search_query,
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
    
    status = 'activated' if product.is_active else 'deactivated'
    messages.success(request, f'Product "{product.name}" {status} successfully!')
    return redirect('dashboard_products')


@superuser_required
def product_delete(request, pk):
    """Delete product"""
    product = get_object_or_404(Juice, pk=pk)
    product_name = product.name
    product.delete()
    messages.success(request, f'Product "{product_name}" deleted successfully!')
    return redirect('dashboard_products')


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
