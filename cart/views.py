from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from food.models import FoodItem
from .serializers import CartItemSerializer
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Cart, CartItem
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status  # for HTTP status codes
from rest_framework.permissions import AllowAny



class CartCreateApiView(APIView):
    permission_classes = [permissions.AllowAny]
    

    def post(self, request, format=None):
        serializer = serializers.CartCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cart Created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, format=None):
        objects = Cart.objects.all()
        print(objects)
        serializer = serializers.CartCreateSerializer(objects, many=True)
        return Response(serializer.data)


class CartDetailsView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, pk, format=None):
        print("Pk" ,pk)
        object = Cart.objects.get(user = pk)
        print(object)
        serializer = serializers.CartCreateSerializer(object)
        return Response(serializer.data)
    
class AddFoodIntoCartWithCartId(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        cart_items = CartItem.objects.all()
        serializer = serializers.CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.CartItemsUpdateSerializer(data=request.data)

        if serializer.is_valid():
            food = FoodItem.objects.get(pk=request.data['food_item'])

            # Check if the cart item already exists
            cart_item = CartItem.objects.filter(cart=request.data['cart'], food_item=request.data['food_item']).first()

            if cart_item:
                # If the cart item exists, update it
                cart_item.quantity += 1  # Default increase by 1 if it's added again
                cart_item.price = cart_item.quantity * float(food.price)
                cart_item.save()
                return Response('Cart item updated', status=200)

            # If the cart item doesn't exist, create it with default quantity = 1
            cart_item = serializer.save()
            cart_item.quantity = 1  # Ensure it's always added with a quantity of 1
            cart_item.price = cart_item.quantity * float(food.price)
            cart_item.save()

            return Response('Food added to cart', status=201)
        else:
            return Response(serializer.errors, status=400)

    
class SeeCartItemAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, cart_id, format=None):
            cart = Cart.objects.get(id=cart_id)
            cart_items = CartItem.objects.filter(cart=cart)
            print("Cart Items", cart_items)
            serializer = serializers.CartItemSerializer(cart_items, many=True)
            return Response(serializer.data, status=200)

    
class SeeCartItemforSellerAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, cart_id, seller_id, format=None):
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=404)
        cart_items = CartItem.objects.filter(cart=cart, food_item__seller__id=seller_id)

        if not cart_items.exists():
            return Response({"message": "No items found for this seller in the cart"}, status=404)

        serializer = CartItemSerializer(cart_items, many=True)

        return Response(serializer.data, status=200)

    

         
class CartItemsUpdate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def get(self, request, pk, format=None):
        try:
            obj = CartItem.objects.get(pk=pk)
            serializer = CartItemSerializer(obj)
            return Response(serializer.data, status=200)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=404)

    def delete(self, request, pk, format=None):
        try:
            obj = CartItem.objects.get(pk=pk)
            cart_id = obj.cart.id
            obj.delete()

            # Fetch updated cart items
            cart_items = CartItem.objects.filter(cart=cart_id)
            updated_cart_items = serializers.CartItemSerializer(cart_items, many=True).data
            return Response({"cart_items": updated_cart_items}, status=200)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=404)


class ClearCartItemsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self, request, cart_id, seller_id, format=None):
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get cart items related to the seller
        cart_items = CartItem.objects.filter(cart=cart, food_item__seller__id=seller_id)

        if not cart_items.exists():
            return Response({"message": "No cart items found for this seller"}, status=status.HTTP_404_NOT_FOUND)

        # Delete the filtered cart items
        cart_items.delete()

        return Response({"message": "Cart items for this seller deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
