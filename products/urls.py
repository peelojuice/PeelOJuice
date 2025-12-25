from django.urls import path
from .views import CategoryListAPIView, JuiceListAPIView, JuiceDetailAPIView, BranchListAPIView, BranchProductsAPIView
from .views_admin import (
    ToggleJuiceAvailabilityAPIView,
    ToggleJuiceActiveAPIView,
    UpdateJuicePriceAPIView
)

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('juices/', JuiceListAPIView.as_view(), name='juice-list'),
    path('juices/<int:pk>/', JuiceDetailAPIView.as_view(), name='juice-detail'),
    
    # Branch APIs
    path('branches/', BranchListAPIView.as_view(), name='branch-list'),
    path('branches/<int:branch_id>/products/', BranchProductsAPIView.as_view(), name='branch-products'),
    
    # Admin APIs
    path('admin/juices/<int:pk>/toggle-availability/', ToggleJuiceAvailabilityAPIView.as_view(), name='toggle-juice-availability'),
    path('admin/juices/<int:pk>/toggle-active/', ToggleJuiceActiveAPIView.as_view(), name='toggle-juice-active'),
    path('admin/juices/<int:pk>/update-price/', UpdateJuicePriceAPIView.as_view(), name='update-juice-price'),
]
