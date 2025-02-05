from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from . import serializers
from .models import Seller, Review
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import DISTRICT_CHOICES
from django.db.models import Q

# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
# Create your views here.



class DistrictChoicesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"districts": DISTRICT_CHOICES})




class SellerRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.SellerRegistrationSerializer

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
          
            user = serializer.save()
            print("52 line User", user)
            # seller_id = user.seller.id  # Ensure `user.seller` exists
                
            token = default_token_generator.make_token(user)
            print("token ", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ", uid)

            confirm_link = f"http://127.0.0.1:8000/seller/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            #   "seller_id": seller_id,
            return Response({"message": "Check your mail for confirmation."}, status=201)

        return Response(serializer.errors, status=400)


    
def activate(request, uid64, token):
        try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = User._default_manager.get(pk=uid)
        except(User.DoesNotExist):
            user = None 
        
        if user is not None and default_token_generator.check_token(user, token):
            print( "83 line User ans Token",user, token)
            user.is_active = True
            user.save()
            return redirect('https://sabrina-prity.github.io/Quick_Bite_Frontend/seller_login.html')
        else:
            return redirect('https://sabrina-prity.github.io/Quick_Bite_Frontend/seller_register.html')





class SellerLoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.SellerLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            print("UserName",username)
            print("Password",password)

            user = authenticate(username=username, password=password)
            print("User",user)
            if user:
                print("User1",user)
                if not user.is_active:
                    return Response({'error': "Account is inactive."}, status=403)

                token, _ = Token.objects.get_or_create(user=user)
                login(request, user) 

                seller_id = getattr(user, 'seller', None)
                seller_id = seller_id.id if seller_id else None

                
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    "is_admin": user.is_staff,
                    "seller_id": seller_id,
                }, status=200)
            
            return Response({'error': "Invalid credentials."}, status=401)

        return Response(serializer.errors, status=400)



class SellerLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
    
        request.user.auth_token.delete() 
        logout(request)  
        return Response({"detail": "Logout successful"})
    

    

class SellerListView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        sellers = Seller.objects.all()

        # Get all 'search' query parameters (can be multiple)
        search_queries = request.query_params.getlist('search')

        for search_query in search_queries:
            if search_query:
                sellers = sellers.filter(
                    Q(company_name__icontains=search_query) |
                    Q(district__icontains=search_query) |
                    Q(street_name__icontains=search_query)
                )

        serializer = serializers.SellerGetSerializer(sellers, many=True)
        return Response(serializer.data)
    

class SellerDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):  
        try:
            seller = Seller.objects.get(pk=pk)  
            print(seller)
            serializer = serializers.SellerSerializer(seller)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Seller.DoesNotExist:
            return Response({"detail": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        seller = Seller.objects.get(pk=pk)
        serializer = serializers.SellerSerializer(seller, data=request.data, partial=True)  # allow partial updates

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        seller = Seller.objects.get(pk=pk)
        seller.delete()
        return Response({"detail": "Seller deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class SellerDetailsUpdateView(APIView):
    permission_classes = [permissions.AllowAny]  

    def get(self, request, seller_id):
        try:
            seller = Seller.objects.get(pk=seller_id)
            serializer = serializers.SellerSerializer(seller)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Seller.DoesNotExist:
            return Response({"detail": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)

    
    def put(self, request, seller_id):
        try:
            seller = Seller.objects.get(pk=seller_id)
            serializer = serializers.SellerSerializer(seller, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Seller.DoesNotExist:
            return Response({"detail": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)

class SellerReviewListCreateDeleteView(APIView):
    permission_classes = [permissions.AllowAny]  

    def get(self, request, seller_id):
        try:
            reviews = Review.objects.filter(seller_id=seller_id)  
            if not reviews.exists(): 
                return Response({"detail": "No reviews found for this seller."}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = serializers.ReviewGetSerializer(reviews, many=True)  # Set many=True for multiple objects
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, seller_id):
        try:
            review_id = request.data.get("id")  # Expecting review ID in the request data
            review = Review.objects.get(id=review_id, seller_id=seller_id)
            serializer = serializers.ReviewSerializer(review, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Review.DoesNotExist:
            return Response({"detail": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


    def post(self, request, seller_id):
        data = request.data
        data["seller"] = seller_id  
        data["user"] = request.user.id if request.user.is_authenticated else None

        serializer = serializers.ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, seller_id, pk):
        try:
            review = Review.objects.get(pk=pk, seller_id=seller_id)
            review.delete()
            return Response(
                {"message": "Review deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )

        except Review.DoesNotExist:
            return Response(
                {"error": "Review not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        



    # def delete(self, request, seller_id, review_id):
    #     # Ensure the review exists and belongs to the current user
    #     review = get_object_or_404(Review, id=review_id, food_item_id=seller_id)
    #     if review.user != request.user:
    #         return Response({"error": "You can only delete your own reviews."}, status=status.HTTP_403_FORBIDDEN)

    #     # Delete the review
    #     review.delete()
    #     return Response({"message": "Review deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
