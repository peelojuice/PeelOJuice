from django.db import models
from django.conf import settings
from products.models import Juice
from decimal import Decimal


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    applied_coupon = models.ForeignKey(
        'coupons.Coupon',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='carts'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        return sum(
            (item.price_at_added * item.quantity)
            for item in self.items.all()
        ) or Decimal('0.00')

    def __str__(self):
        return f"Cart of {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    juice = models.ForeignKey(
        Juice,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    price_at_added = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    cooking_instructions = models.CharField(
        max_length=200,
        blank=True,
        default='',
        help_text='Special cooking instructions (e.g., less sugar, extra ice)'
    )

    class Meta:
        unique_together = ('cart', 'juice')

    def __str__(self):
        return f"{self.juice.name} {self.quantity}"
