from django.urls import path
from . import views

urlpatterns = [
    # Dashboard home
    path('', views.dashboard_home, name='dashboard_home'),
    
    # Products
    path('products/', views.product_list, name='dashboard_products'),
    path('products/add/', views.product_add, name='dashboard_product_add'),
    path('products/<int:pk>/edit/', views.product_edit, name='dashboard_product_edit'),
    path('products/<int:pk>/toggle/', views.product_toggle_status, name='dashboard_product_toggle'),
    path('products/<int:pk>/delete/', views.product_delete, name='dashboard_product_delete'),
    path('products/<int:product_id>/branch/<int:branch_id>/toggle/', views.toggle_branch_availability, name='dashboard_toggle_branch_availability'),
    
    # Orders
    path('orders/', views.order_list, name='dashboard_orders'),
    path('orders/<int:order_id>/update-status/', views.order_update_status, name='dashboard_order_update_status'),
    
    # Payments
    path('payments/', views.payment_list, name='dashboard_payments'),
    path('payments/<int:payment_id>/update-status/', views.payment_update_status, name='dashboard_payment_update_status'),
    
    # Users
    path('users/', views.user_list, name='dashboard_users'),
    path('users/add/', views.user_add, name='dashboard_user_add'),
    path('users/<int:pk>/edit/', views.user_edit, name='dashboard_user_edit'),
]
