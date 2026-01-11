from django.db import models
from django.conf import settings
from products.models import Juice
from decimal import Decimal


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    
    # Sequential order number for user-facing display (1, 2, 3, etc.)
    order_number = models.PositiveIntegerField(
        unique=True,
        editable=False,
        null=True,  # Temporarily allow null for migration
        help_text="Sequential order number shown to users"
    )
    
    # Branch this order is for
    branch = models.ForeignKey(
        'products.Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        help_text="Branch from which this order will be fulfilled"
    )

    # Delivery Address
    address = models.ForeignKey(
        'addresses.Address',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        help_text="Delivery address for this order"
    )
    
    food_subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Total food cost before GST"
    )
    food_gst = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="5% GST on food (collected by platform)"
    )
    
    delivery_fee_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Delivery fee before GST"
    )
    delivery_gst = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="18% GST on delivery fee"
    )
    
    platform_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=10,
        help_text="Platform fee (includes 18% GST)"
    )
    
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Final payable amount"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def food_total(self):
        """Food cost + 5% GST"""
        return self.food_subtotal + self.food_gst
    
    @property
    def delivery_total(self):
        """Delivery fee + 18% GST"""
        return self.delivery_fee_base + self.delivery_gst

    def calculate_totals(self):
        """Calculate all GST and totals"""
        # Apply discount to subtotal first
        discounted_subtotal = self.food_subtotal - self.discount
        
        # Calculate GST on discounted amount
        self.food_gst = (discounted_subtotal * Decimal('0.05')).quantize(Decimal('0.01'))
        self.delivery_gst = (self.delivery_fee_base * Decimal('0.18')).quantize(Decimal('0.01'))
        
        self.total_amount = (
            discounted_subtotal + 
            self.food_gst + 
            self.delivery_fee_base + 
            self.delivery_gst + 
            self.platform_fee
        )

    def save(self, *args, **kwargs):
        """Override save to auto-assign sequential order number"""
        if not self.order_number:
            # Get the highest order number and add 1
            last_order = Order.objects.all().order_by('-order_number').first()
            if last_order and last_order.order_number:
                self.order_number = last_order.order_number + 1
            else:
                self.order_number = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_number} - {self.user.email} - ₹{self.total_amount}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    juice = models.ForeignKey(
        Juice,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField()
    price_per_item = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Price at time of order"
    )
    cooking_instructions = models.CharField(
        max_length=200,
        blank=True,
        default='',
        help_text='Special cooking instructions from customer'
    )

    @property
    def subtotal(self):
        return self.price_per_item * self.quantity

    def __str__(self):
        return f"{self.juice.name} x{self.quantity}"
