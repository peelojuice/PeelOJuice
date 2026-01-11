from django.urls import path
from .views import AddToCartAPIView, ViewCartAPIView, UpdateCartItemAPIView, RemoveCartItemAPIView, ApplyCouponAPIView, RemoveCouponAPIView, UpdateItemInstructionsAPIView

urlpatterns = [
    path('', ViewCartAPIView.as_view(), name='view-cart'),
    path('add/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('update/', UpdateCartItemAPIView.as_view(), name='update-cart-item'),
    path('remove/', RemoveCartItemAPIView.as_view(), name='remove-cart-item'),
    path('apply-coupon/', ApplyCouponAPIView.as_view(), name='apply-coupon'),
    path('remove-coupon/', RemoveCouponAPIView.as_view(), name='remove-coupon'),
    path('update-instructions/', UpdateItemInstructionsAPIView.as_view(), name='update-instructions'),
]
