from django.urls import path
from .views import (
    CheckoutAPIView, 
    MyOrdersAPIView, 
    OrderDetailAPIView, 
    CancelOrderAPIView,
    UpdateOrderStatusAPIView
)

urlpatterns = [
    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('my-orders/', MyOrdersAPIView.as_view(), name='my-orders'),
    path('my-orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('my-orders/<int:pk>/cancel/', CancelOrderAPIView.as_view(), name='cancel-order'),
    path('admin/orders/<int:pk>/update-status/', UpdateOrderStatusAPIView.as_view(), name='admin-update-order-status'),
]
