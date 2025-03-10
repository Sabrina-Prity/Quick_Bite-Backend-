from rest_framework import serializers
from django.contrib.auth.models import User
from . import models
from .models import FoodItem
from seller.serializers import SellerSerializer
from customer.serializers import CustomerSerializer
from rest_framework import serializers
from .models import Comment


class FoodItemGetSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    category = serializers.StringRelatedField(many=False)
    seller = SellerSerializer(many=False)
    class Meta:
        model = models.FoodItem
        fields = '__all__'

class FoodItemSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    category = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.FoodItem
        fields = '__all__'



class AllCommentSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source="food_item.name", read_only=True)  # Fetch food name

    class Meta:
        model = Comment
        fields = ['id', 'user', 'food_name', 'body', 'rating', 'created_on']  # Use `body` instead of `text`
 

class CommentSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()
    # user = CustomerSerializer()
      
    class Meta:
        model = models.Comment
        fields = '__all__'

class CommentGetSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    # user = CustomerSerializer()
      
    class Meta:
        model = models.Comment
        fields = '__all__'