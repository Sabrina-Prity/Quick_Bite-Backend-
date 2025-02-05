from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from . import serializers
from .models import Customer
from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to QuickBite API!")

class CustomerRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.CustomerRegistrationSerializer

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

            # Generate token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # You can optionally send these in the response, if needed
            return Response({
                "message": "Registration successful",
                "token": token,
                "uid": uid
            })

        return Response(serializer.errors, status=400)

    

        


class CustomerLoginApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.CustomerLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)  
                
                return Response({
                    'token': token.key, 
                    'user_id': user.id, 
                    "is_admin": user.is_staff,
                })
            else:
                return Response({'error': "Invalid Credential"})

        return Response(serializer.errors)




class CustomerLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
    
        request.user.auth_token.delete() 
        logout(request)  
        return Response({"detail": "Logout successful"})
    

class CustomerListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        customers = Customer.objects.all()
        serializer = serializers.CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    

class CustomerDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, user_id):
        try:
            customer = Customer.objects.get(user_id=user_id)
            serializer = serializers.CustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"detail": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

   
    def put(self, request, user_id):
            customer = Customer.objects.get(user_id=user_id)
            serializer = serializers.CustomerSerializer(customer, data=request.data, partial=True)  # allow partial updates

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    def delete(self, request, user_id):
            customer = Customer.objects.get(user_id=user_id)
            customer.delete()
            return Response({"detail": "Customer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
       

