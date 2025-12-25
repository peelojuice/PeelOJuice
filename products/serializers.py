from rest_framework import serializers
from .models import Category, Juice, Branch

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'city', 'state', 'pincode', 
                  'phone', 'email', 'opening_time', 'closing_time', 'is_active']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class JuiceSerializer(serializers.ModelSerializer):
    category = CategoryMiniSerializer(read_only=True)
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Juice
        fields = [
            'id',
            'name',
            'price',
            'description',
            'long_description',
            'image',
            'is_available',
            'category',
            'net_quantity_ml',
            'features',
            'benefits',
            'nutrition_calories',
            'nutrition_total_fat',
            'nutrition_carbohydrate',
            'nutrition_dietary_fiber',
            'nutrition_total_sugars',
            'nutrition_protein',
            'ingredients',
            'allergen_info'
        ]