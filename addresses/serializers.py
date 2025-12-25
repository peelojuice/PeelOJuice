from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'label', 'full_name', 'phone_number', 'address_line1', 
                  'address_line2', 'city', 'state', 'pincode', 'landmark', 
                  'is_default', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Automatically assign the user from the request context
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
