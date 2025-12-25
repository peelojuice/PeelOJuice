from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from dashboard.decorators import superuser_required
from users.models import User


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
    users = paginator.get_page(page_number)
    
    context = {
        'users': users,
        'search_query': search_query,
    }
    
    return render(request, 'dashboard/users/list.html', context)


@superuser_required
def user_add(request):
    """Add new user with role assignment"""
    from products.models import Branch
    
    if request.method == 'POST':
        email = request.POST.get('email')
        full_name = request.POST.get('full_name', '')
        phone_number = request.POST.get('phone_number', '')
        password = request.POST.get('password')
        is_active = request.POST.get('is_active') == 'on'
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'
        assigned_branch_id = request.POST.get('assigned_branch', '')
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, f'User with email "{email}" already exists!')
            branches = Branch.objects.filter(is_active=True)
            return render(request, 'dashboard/users/form.html', {'branches': branches})
        
        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                full_name=full_name,
                phone_number=phone_number,
                is_active=is_active,
                is_staff=is_staff,
                is_superuser=is_superuser,
            )
            
            # Assign branch if staff and branch selected
            if is_staff and assigned_branch_id:
                try:
                    branch = Branch.objects.get(id=assigned_branch_id, is_active=True)
                    user.assigned_branch = branch
                    user.save()
                except Branch.DoesNotExist:
                    pass
            
            messages.success(request, f'User "{user.email}" created successfully!')
            return redirect('dashboard_users')
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
    
    branches = Branch.objects.filter(is_active=True)
    return render(request, 'dashboard/users/form.html', {'branches': branches})


@superuser_required
def user_edit(request, pk):
    """Edit user roles and permissions"""
    from products.models import Branch
    
    user_obj = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        user_obj.full_name = request.POST.get('full_name', '')
        user_obj.phone_number = request.POST.get('phone_number', '')
        user_obj.is_active = request.POST.get('is_active') == 'on'
        user_obj.is_staff = request.POST.get('is_staff') == 'on'
        user_obj.is_superuser = request.POST.get('is_superuser') == 'on'
        user_obj.is_email_verified = request.POST.get('is_email_verified') == 'on'
        user_obj.is_phone_verified = request.POST.get('is_phone_verified') == 'on'
        
        # Handle branch assignment for staff
        assigned_branch_id = request.POST.get('assigned_branch', '')
        if user_obj.is_staff and assigned_branch_id:
            try:
                branch = Branch.objects.get(id=assigned_branch_id, is_active=True)
                user_obj.assigned_branch = branch
            except Branch.DoesNotExist:
                user_obj.assigned_branch = None
        else:
            user_obj.assigned_branch = None
        
        try:
            user_obj.save()
            messages.success(request, f'User "{user_obj.email}" updated successfully!')
            return redirect('dashboard_users')
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')
    
    branches = Branch.objects.filter(is_active=True)
    context = {'user_obj': user_obj, 'branches': branches}
    return render(request, 'dashboard/users/form.html', context)
