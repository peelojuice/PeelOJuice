from django.contrib import admin
from .models import Category, Juice, Branch, BranchProduct


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('is_active',)
    actions = ['activate_categories', 'deactivate_categories']

    def activate_categories(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} category(ies) activated.')
    activate_categories.short_description = 'Activate selected categories'

    def deactivate_categories(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} category(ies) deactivated.')
    deactivate_categories.short_description = 'Deactivate selected categories'


@admin.register(Juice)
class JuiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'category',
        'is_available',
        'is_active',
        'created_at',
    )
    list_filter = ('is_available', 'is_active', 'category')
    search_fields = ('name', 'category__name')
    list_editable = ('is_available', 'is_active', 'price')
    actions = [
        'mark_as_available',
        'mark_as_unavailable',
        'activate_juices',
        'deactivate_juices'
    ]

    def mark_as_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f'{updated} juice(s) marked as available.')
    mark_as_available.short_description = 'Mark selected as Available'

    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f'{updated} juice(s) marked as unavailable.')
    mark_as_unavailable.short_description = 'Mark selected as Unavailable'

    def activate_juices(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} juice(s) activated.')
    activate_juices.short_description = 'Activate selected juices'

    def deactivate_juices(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} juice(s) deactivated.')
    deactivate_juices.short_description = 'Deactivate selected juices'


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'city']
    search_fields = ['name', 'city', 'phone']
    list_editable = ['is_active']


@admin.register(BranchProduct)
class BranchProductAdmin(admin.ModelAdmin):
    list_display = ['branch', 'product', 'is_available', 'updated_at']
    list_filter = ['branch', 'is_available']
    search_fields = ['branch__name', 'product__name']
    list_editable = ['is_available']
