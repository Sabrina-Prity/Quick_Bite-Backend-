from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from .models import FoodItem, Comment
from .serializers import FoodItemSerializer,AllCommentSerializer, CommentSerializer, CommentGetSerializer
from category.models import Category
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q
from .serializers import CommentGetSerializer, CommentSerializer


class FoodItemCreateView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, seller_id):
        serializer = FoodItemSerializer(data=request.data)

        if serializer.is_valid():
            category_id = request.data.get('category')

            if category_id:
                try:
                    # Validate if the category exists for the given seller
                    category = Category.objects.get(id=category_id, seller_id=seller_id)

                    # Save the food item with the seller_id from the URL
                    serializer.save(category=category, seller_id=seller_id)
                    return Response(serializer.data, status=201)

                except Category.DoesNotExist:
                    return Response({"error": "Category does not exist for the provided seller."}, status=400)
            else:
                return Response({"error": "'category' is required."}, status=400)

        return Response(serializer.errors, status=400)


    

class FoodItemDeleteView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        food_item = FoodItem.objects.filter(pk=pk)

        if not food_item.exists():
            return Response("Food item not found")
        else:
            serializer = FoodItemSerializer(food_item, many=True)
            return Response(serializer.data)

    def delete(self, request, pk, seller_id):
        try:
           
            food_item = FoodItem.objects.get(pk=pk)
            if food_item.seller_id != seller_id:
                return Response({"error": "You are not authorized to delete this food item."}, status=403)

            food_item.delete()
            return Response({"message": "Food item deleted successfully."}, status=204)

        except FoodItem.DoesNotExist:
            return Response({"error": "Food item not found."}, status=404)
        



class FoodItemListpecificSellerView(APIView):
    permission_classes = [permissions.AllowAny]  
    def get(self, request, seller_id):
        # Get all 'search' query parameters
        search_params = request.query_params.getlist('search', [])

        food_items = FoodItem.objects.filter(seller_id=seller_id)

        if search_params:
            query = Q()
            for search_term in search_params:
                query |= Q(name__icontains=search_term) | Q(category__name__icontains=search_term)
            food_items = food_items.filter(query)

        if not food_items.exists():
            return Response({"error": "No food items found for this seller with the given search criteria."}, status=404)

        serializer = FoodItemSerializer(food_items, many=True)
        return Response(serializer.data)
    

class AllCommentView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        Retrieve all comments with food name.
        """
        comments = Comment.objects.select_related('food_item').all()  # Optimized query
        serializer = AllCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class CommentListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, food_id=None, seller_id=None):
        if seller_id and food_id:
            food_item = get_object_or_404(FoodItem, id=food_id, seller_id=seller_id)
            comments = Comment.objects.filter(food_item=food_item)
        elif seller_id:
            food_items = FoodItem.objects.filter(seller_id=seller_id)
            comments = Comment.objects.filter(food_item__in=food_items)
        elif food_id:
            comments = Comment.objects.filter(food_item_id=food_id)
        else:
            return Response({"error": "Food ID or Seller ID is required."}, status=400)

        serializer = CommentGetSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, food_id=None, seller_id=None):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            # Ensure food ID and seller ID exist in the URL
            if not food_id:
                raise ValidationError({"error": "Food ID is required."})
            if not seller_id:
                raise ValidationError({"error": "Seller ID is required."})

            # Validate the food item and its association with the seller
            food_item = get_object_or_404(FoodItem, id=food_id, seller_id=seller_id)
            user = request.user if request.user.is_authenticated else None  # Optionally link the logged-in user

            serializer.save(user=user, food_item=food_item)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    


class CommentUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        if comment.user != request.user:
            raise PermissionDenied({"error": "You do not have permission to update this comment."})

        # Serialize and validate the request data
        serializer = CommentSerializer(comment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        if comment.user != request.user:
            raise PermissionDenied({"error": "You do not have permission to delete this comment."})

        # Delete the comment
        comment.delete()
        return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    


