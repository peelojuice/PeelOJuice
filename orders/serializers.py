from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    juice_name = serializers.CharField(source='juice.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'juice',
            'juice_name',
            'quantity',
            'price_per_item',
            'subtotal'
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'order_number',
            'status',
            'food_subtotal',
            'food_gst',
            'delivery_fee_base',
            'delivery_gst',
            'platform_fee',
            'discount',
            'total_amount',
            'created_at',
            'items'
        )

class MyOrderListSerializer(serializers.ModelSerializer):
    total_items = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, read_only=True)
    payment_method = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'order_number',
            'status',
            'total_amount',
            'payment_method',
            'created_at',
            'total_items',
            'items'
        )

    def get_total_items(self, obj):
        return obj.items.count()
    
    def get_payment_method(self, obj):
        if hasattr(obj, 'payment'):
            return obj.payment.get_method_display()
        return 'N/A'

class OrderItemDetailSerializer(serializers.ModelSerializer):
    juice_name = serializers.CharField(source='juice.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            'juice_name',
            'quantity',
            'price_per_item',
            'subtotal'
        )

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    can_cancel = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'items',
            'status',
            'status_display',
            'food_subtotal',
            'food_gst',
            'delivery_fee_base',
            'delivery_gst',
            'platform_fee',
            'discount',
            'total_amount',
            'payment_method',
            'payment_status',
            'can_cancel',
            'created_at',
            'updated_at'
        ]
    
    def get_payment_method(self, obj):
        if hasattr(obj, 'payment'):
            return obj.payment.get_method_display()
        return 'N/A'
    
    def get_payment_status(self, obj):
        if hasattr(obj, 'payment'):
            return obj.payment.status
        return 'N/A'
    
    def get_can_cancel(self, obj):
        return obj.status not in ['delivered', 'cancelled']
