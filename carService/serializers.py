from rest_framework import serializers
from .models import CustomUser, District, Address, Order, OrderAnalysis


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password',
                  'avatar',
                  'user_type',
                  'is_superuser',
                  'is_staff',
                  'first_name',
                  'last_name',
                  'is_active',
                  'date_joined',
                  'last_login'
                  ]

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'date_time_ordered', 'address_from', 'address_to', 'order_status', 'driver', 'get_address_from', 'get_address_to']


class OrderAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAnalysis
        fields = '__all__'