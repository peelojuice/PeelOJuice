from django.contrib import admin
from .models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['label', 'full_name', 'user', 'city', 'is_default', 'created_at']
    list_filter = ['is_default', 'city', 'state']
    search_fields = ['full_name', 'user__email', 'city', 'pincode']
    readonly_fields = ['created_at', 'updated_at']
