from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


def superuser_required(view_func):
    """
    Decorator that restricts access to superusers only.
    Redirects unauthenticated users to web login.
    Redirects non-superusers to home page with error message.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            # Redirect to web login with next parameter
            login_url = reverse('web_login')
            next_url = request.get_full_path()
            return redirect(f'{login_url}?next={next_url}')
        
        # Check if user is superuser
        if not request.user.is_superuser:
            messages.error(request, 'Access denied. Superuser privileges required.')
            return redirect('dashboard_home')
        
        return view_func(request, *args, **kwargs)
    return wrapper
