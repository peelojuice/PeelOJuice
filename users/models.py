from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,email,phone_number,password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not phone_number:
            raise ValueError("Phone number is required")
        email = self.normalize_email(email)
        user = self.model(email=email,phone_number=phone_number,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,email,phone_number,password, **extra_fields):

        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')  

        return self.create_user(email,phone_number,password, **extra_fields)      

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100,default="",
    blank=True)
    phone_number = models.CharField(max_length=12,unique=True)
    email_otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    phone_otp = models.CharField(max_length=6, null=True, blank=True)
    phone_otp_created_at = models.DateTimeField(null=True, blank=True)
    
    password_reset_otp = models.CharField(max_length=6, null=True, blank=True)
    password_reset_otp_created_at = models.DateTimeField(null=True, blank=True)
    password_reset_otp_verified = models.BooleanField(default=False)

    otp_failed_attempts = models.IntegerField(default=0)
    otp_locked_until = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Branch assignment for staff members
    assigned_branch = models.ForeignKey(
        'products.Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_members',
        help_text="Branch this staff member is assigned to (for branch-specific access)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    def get_full_name(self):
        """Return the full name or email if full name is empty"""
        return self.full_name if self.full_name else self.email
    
    def __str__(self):
        return self.email
