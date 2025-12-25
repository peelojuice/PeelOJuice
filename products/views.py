from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Juice, Category, Branch, BranchProduct
from .serializers import JuiceSerializer, CategorySerializer, BranchSerializer
from django.shortcuts import get_object_or_404

class CategoryListAPIView(APIView):

    def get(self, request):
        categories = Category.objects.filter(is_active=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class JuicePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class JuiceListAPIView(APIView):
    pagination_class = JuicePagination

    def get(self, request):
        category_id = request.query_params.get('category_id')

        juices = Juice.objects.filter(is_active=True)

        if category_id:
            juices = juices.filter(category_id=category_id)

        paginator = JuicePagination()
        paginated_juices = paginator.paginate_queryset(juices, request)
        serializer = JuiceSerializer(paginated_juices, many=True)
        return paginator.get_paginated_response(serializer.data)


class JuiceDetailAPIView(APIView):

    def get(self, request, pk):
        juice = get_object_or_404(Juice, pk=pk, is_active=True)
        serializer = JuiceSerializer(juice)
        return Response(serializer.data)


class BranchListAPIView(APIView):
    """Get all active branches"""
    def get(self, request):
        branches = Branch.objects.filter(is_active=True).order_by('city', 'name')
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data)




class BranchProductsAPIView(APIView):
    """Get all available products for a specific branch with pagination"""
    pagination_class = JuicePagination
    
    def get(self, request, branch_id):
        try:
            branch = Branch.objects.get(id=branch_id, is_active=True)
        except Branch.DoesNotExist:
            return Response(
                {'error': 'Branch not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get only available products at this branch
        branch_products = BranchProduct.objects.filter(
            branch=branch,
            is_available=True,
            product__is_active=True
        ).select_related('product', 'product__category')
        
        # Filter by category if provided
        category_id = request.query_params.get('category_id')
        if category_id:
            branch_products = branch_products.filter(product__category_id=category_id)
        
        products = [bp.product for bp in branch_products]
        
        # Apply pagination
        paginator = JuicePagination()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = JuiceSerializer(paginated_products, many=True)
        
        return paginator.get_paginated_response(serializer.data)
