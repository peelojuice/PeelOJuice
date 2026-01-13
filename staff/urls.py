from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.staff_login_view, name='staff_login'),
    path('logout/', views.staff_logout_view, name='staff_logout'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('orders/', views.staff_orders_list, name='staff_orders_list'),
    path('orders/<int:pk>/', views.staff_order_detail, name='staff_order_detail'),
    
    # REST API endpoints for mobile app
    path('api/branch-products/', views.StaffBranchProductsAPIView.as_view(), name='staff_branch_products_api'),
    path('api/branch-products/<int:branch_product_id>/toggle/', views.ToggleBranchProductAvailabilityAPIView.as_view(), name='toggle_branch_product_api'),
]
