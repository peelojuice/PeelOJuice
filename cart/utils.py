from .models import Cart

def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(
        user=user,
        is_active=True
    )
    return cart

def get_cart_total(cart):
    return sum(
        item.price_at_added * item.quantity
        for item in cart.items.all()
    )
