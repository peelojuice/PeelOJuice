# Import all views from submodules for easy access
from .home import dashboard_home
from .products import (
    product_list,
    product_add,
    product_edit,
    product_toggle_status,
    product_delete,
    toggle_branch_availability,
)
from .orders import (
    order_list,
    order_update_status,
)
from .payments import (
    payment_list,
    payment_update_status,
)
from .users import user_list, user_add, user_edit

__all__ = [
    # Home
    'dashboard_home',
    # Products
    'product_list',
    'product_add',
    'product_edit',
    'product_toggle_status',
    'product_delete',
    'toggle_branch_availability',
    # Orders
    'order_list',
    'order_update_status',
    # Payments
    'payment_list',
    'payment_update_status',
    # Users
    'user_list',
    'user_add',
    'user_edit',
]
