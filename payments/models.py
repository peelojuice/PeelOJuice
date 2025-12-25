from django.db import models
from django.conf import settings
from orders.models import Order


class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
    )
    
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHODS,
        default='cod'
    )
    status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS,
        default='pending'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    transaction_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Payment gateway transaction ID (null for COD)"
    )
    razorpay_order_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Razorpay order ID"
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment #{self.id} - Order #{self.order.id} - {self.method} - {self.status}"
