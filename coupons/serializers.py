from rest_framework import serializers
from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    discount_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_type', 'discount_value', 'discount_display', 'min_order_value', 'max_discount']
    
    def get_discount_display(self, obj):
        if obj.discount_type == 'percentage':
            return f"{obj.discount_value}%"
        return f"₹{obj.discount_value}"


class ValidateCouponSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)
    cart_total = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
