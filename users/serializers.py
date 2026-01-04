from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    assigned_branch = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'phone_number', 
            'is_email_verified', 'is_phone_verified', 'created_at',
            'is_staff', 'assigned_branch'
        ]
        read_only_fields = ['id', 'is_email_verified', 'is_phone_verified', 'created_at', 'is_staff', 'assigned_branch']
    
    def get_assigned_branch(self, obj):
        """Return assigned branch details for staff users"""
        if obj.assigned_branch:
            return {
                'id': obj.assigned_branch.id,
                'name': obj.assigned_branch.name,
                'city': obj.assigned_branch.city,
                'address': obj.assigned_branch.address,
                'phone': obj.assigned_branch.phone,
                'email': obj.assigned_branch.email
            }
        return None


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, max_length=150)
    last_name = serializers.CharField(write_only=True, max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'password', 'confirm_password']
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data
    
    def create(self, validated_data):
        # Combine first_name and last_name into full_name
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')
        full_name = f"{first_name} {last_name}".strip()
        
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            full_name=full_name
        )
        return user