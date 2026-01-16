from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)
    fields = ('juice', 'quantity', 'price_per_item', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'user',
        'branch',  # Added to show which branch the order belongs to
        'food_subtotal',
        'food_gst_display',
        'delivery_total_display',
        'platform_fee',
        'total_amount', 
        'status',
        'created_at'
    )
    list_editable = ('status',)
    list_filter = ('status', 'branch', 'created_at')
    search_fields = ('user__email', 'user__full_name', 'id')
    readonly_fields = (
        'food_gst', 
        'delivery_gst', 
        'total_amount', 
        'food_total', 
        'delivery_total',
        'created_at',
        'updated_at'
    )
    
    actions = [
        'mark_as_confirmed',
        'mark_as_preparing',
        'mark_as_out_for_delivery',
        'mark_as_delivered',
        'mark_as_cancelled'
    ]
    
    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'branch', 'address', 'status', 'created_at', 'updated_at')
        }),
        ('Food Charges (5% GST)', {
            'fields': ('food_subtotal', 'food_gst', 'food_total'),
            'description': 'Food cost with 5% GST (collected by platform)'
        }),
        ('Delivery Charges (18% GST)', {
            'fields': ('delivery_fee_base', 'delivery_gst', 'delivery_total'),
            'description': 'Delivery fee with 18% GST'
        }),
        ('Platform & Discounts', {
            'fields': ('platform_fee', 'discount'),
            'description': 'Platform fee already includes 18% GST'
        }),
        ('Total', {
            'fields': ('total_amount',),
        }),
    )
    
    inlines = [OrderItemInline]

    def food_gst_display(self, obj):
        return f"₹{obj.food_gst:.2f} (5%)"
    food_gst_display.short_description = 'Food GST'

    def delivery_total_display(self, obj):
        return f"₹{obj.delivery_total:.2f}"
    delivery_total_display.short_description = 'Delivery Total'

    def mark_as_confirmed(self, request, queryset):
        updated = queryset.exclude(status__in=['cancelled', 'delivered']).update(status='confirmed')
        self.message_user(request, f'{updated} order(s) marked as confirmed.')
    mark_as_confirmed.short_description = 'Mark selected as Confirmed'

    def mark_as_preparing(self, request, queryset):
        updated = queryset.exclude(status__in=['cancelled', 'delivered']).update(status='preparing')
        self.message_user(request, f'{updated} order(s) marked as preparing.')
    mark_as_preparing.short_description = 'Mark selected as Preparing'

    def mark_as_out_for_delivery(self, request, queryset):
        updated = queryset.exclude(status__in=['cancelled', 'delivered']).update(status='out_for_delivery')
        self.message_user(request, f'{updated} order(s) marked as out for delivery.')
    mark_as_out_for_delivery.short_description = 'Mark selected as Out for Delivery'

    def mark_as_delivered(self, request, queryset):
        updated = queryset.exclude(status='cancelled').update(status='delivered')
        self.message_user(request, f'{updated} order(s) marked as delivered.')
    mark_as_delivered.short_description = 'Mark selected as Delivered'

    def mark_as_cancelled(self, request, queryset):
        updated = queryset.exclude(status='delivered').update(status='cancelled')
        self.message_user(request, f'{updated} order(s) marked as cancelled.')
    mark_as_cancelled.short_description = 'Mark selected as Cancelled'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'juice', 'quantity', 'price_per_item', 'subtotal')
    list_filter = ('juice',)
