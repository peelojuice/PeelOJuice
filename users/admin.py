from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ('email', 'phone_number', 'full_name', 'assigned_branch', 'is_email_verified', 'is_phone_verified', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_email_verified', 'is_phone_verified', 'assigned_branch')
    list_editable = ('is_active',)
    
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'full_name', 'password')}),
        ('Verification', {'fields': ('is_email_verified', 'is_phone_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Branch Assignment', {'fields': ('assigned_branch',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

    search_fields = ('email', 'phone_number')
    ordering = ('email',)
    
    actions = [
        'activate_users',
        'deactivate_users',
        'verify_email',
        'verify_phone',
        'reset_otp_lock'
    ]

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} user(s) activated.')
    activate_users.short_description = 'Activate selected users'

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} user(s) deactivated.')
    deactivate_users.short_description = 'Deactivate selected users'

    def verify_email(self, request, queryset):
        updated = queryset.update(is_email_verified=True)
        self.message_user(request, f'{updated} user(s) email verified.')
    verify_email.short_description = 'Verify email for selected users'

    def verify_phone(self, request, queryset):
        updated = queryset.update(is_phone_verified=True)
        self.message_user(request, f'{updated} user(s) phone verified.')
    verify_phone.short_description = 'Verify phone for selected users'

    def reset_otp_lock(self, request, queryset):
        updated = queryset.update(otp_failed_attempts=0, otp_locked_until=None)
        self.message_user(request, f'{updated} user(s) OTP lock reset.')
    reset_otp_lock.short_description = 'Reset OTP lock for selected users'

