from django.shortcuts import render
from rest_framework import viewsets
from . import models
from .models import Category
from .serializers import CategorySerializer
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from rest_framework import filters, pagination
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication

class CategoryAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk=None):
        if pk:  
            try:
                category = Category.objects.get(pk=pk)
                serializer = CategorySerializer(category)
                return Response(serializer.data)
            except Category.DoesNotExist:
                return Response({"detail": "Category not found!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)

    def post(self, request):
        category_name = request.data.get('name')

        if Category.objects.filter(name=category_name).exists():
            return Response(
                {"error": "Category with this name already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk:
            try:
                category = Category.objects.get(pk=pk)
                category.delete()
                return Response({"detail": "Category deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
            except Category.DoesNotExist:
                return Response({"detail": "Category not found!"}, status=status.HTTP_404_NOT_FOUND)
            

class SellerCategoryAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, seller_id):
        # Filter categories by seller_id
        categories = Category.objects.filter(seller_id=seller_id)
        if not categories.exists():
            return Response({"detail": "No categories found for this seller."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, seller_id):
        data = request.data
        data['seller'] = seller_id  

        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, seller_id, pk):
        try:
            category = Category.objects.get(pk=pk, seller_id=seller_id)
            category.delete()
            return Response({"detail": "Category deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"detail": "Category not found!"}, status=status.HTTP_404_NOT_FOUND)
