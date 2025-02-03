from rest_framework import serializers
from . import models
from food.serializers import FoodItemGetSerializer
from food.models import FoodItem

class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    food_item = FoodItemGetSerializer()
    class Meta:
        model = models.CartItem
        fields = "__all__"


class CartItemsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = "__all__"
        # fields = ['id', 'food_item', 'quantity', 'price']


class CartItemForOrderSerializer(serializers.ModelSerializer):
    food_item = serializers.PrimaryKeyRelatedField(queryset=FoodItem.objects.all())
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = models.CartItem
        fields = ['food_item', 'quantity', 'price']



