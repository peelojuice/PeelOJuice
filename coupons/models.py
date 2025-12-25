from django.db import models
from django.utils import timezone
from decimal import Decimal


class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    code = models.CharField(max_length=50, unique=True, help_text="Coupon code (e.g., SAVE10)")
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    discount_value = models.DecimalField(max_digits=8, decimal_places=2, help_text="Percentage (e.g., 10 for 10%) or fixed amount")
    
    min_order_value = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Minimum cart value required")
    max_discount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Maximum discount amount (for percentage coupons)")
    
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField(null=True, blank=True)
    
    usage_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum number of times this coupon can be used")
    usage_count = models.PositiveIntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.discount_value}{'%' if self.discount_type == 'percentage' else '₹'}"
    
    def is_valid(self):
        """Check if coupon is currently valid"""
        now = timezone.now()
        
        if not self.is_active:
            return False, "This coupon is not active"
        
        if self.valid_from > now:
            return False, "This coupon is not yet valid"
        
        if self.valid_to and self.valid_to < now:
            return False, "This coupon has expired"
        
        if self.usage_limit and self.usage_count >= self.usage_limit:
            return False, "This coupon has reached its usage limit"
        
        return True, "Valid"
    
    def calculate_discount(self, cart_total):
        """Calculate discount amount for given cart total"""
        cart_total = Decimal(str(cart_total))
        
        if cart_total < self.min_order_value:
            return Decimal('0.00')
        
        if self.discount_type == 'percentage':
            discount = (cart_total * self.discount_value) / Decimal('100')
            if self.max_discount:
                discount = min(discount, self.max_discount)
        else:  # fixed
            discount = self.discount_value
        
        # Discount cannot exceed cart total
        return min(discount, cart_total)
