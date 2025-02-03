from rest_framework import serializers
from django.contrib.auth.models import User
from . import models
from .models import Order
from food.serializers import FoodItemSerializer
from customer.serializers import CustomerDetailsGetSerializer
from cart.serializers import CartItemForOrderSerializer, CartItemSerializer



class OrderItemSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer()  # Assuming you also want to serialize the food item

    class Meta:
        model = models.OrderItem
        fields = ['id', 'food_item', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)  # Change 'cart_items' to 'order_items'

    class Meta:
        model = Order
        fields = ['id', 'customer', 'seller', 'order_items', 'buying_status', 'mobile', 'district', 'full_address', 'created_at']

class OrderSeeSerializer(serializers.ModelSerializer):
    customer = CustomerDetailsGetSerializer()
    order_items = OrderItemSerializer(many=True)  # Change 'cart_items' to 'order_items'

    class Meta:
        model = Order
        fields = ['id', 'customer', 'seller', 'order_items', 'buying_status', 'mobile', 'district', 'full_address', 'created_at']


class OrderGetSerializer(serializers.ModelSerializer):
    customer = CustomerDetailsGetSerializer()
    food_items = FoodItemSerializer(many=True, read_only=True)
    # cart_items = CartItemSerializer()
    # seller = serializers.StringRelatedField()
    class Meta:
        model = models.Order
        fields = '__all__'