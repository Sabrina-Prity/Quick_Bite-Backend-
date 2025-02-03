from rest_framework import serializers
from django.contrib.auth.models import User
from . import models
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Seller, Review



class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Seller
        fields = '__all__'

class SellerGetSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Seller
        fields = '__all__'

       


class SellerRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    company_name = serializers.CharField(required=True)
    mobile_no = serializers.CharField(required=True)
    street_name = serializers.CharField(required=True)
    postal_code = serializers.CharField(required=True)
    district = serializers.CharField(required=True)
    image = serializers.CharField(max_length=100,required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 
                  'company_name', 'mobile_no', 'street_name', 'postal_code', 'district', 'image']

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        company_name = self.validated_data['company_name']
        mobile_no = self.validated_data['mobile_no']
        street_name = self.validated_data['street_name']
        postal_code = self.validated_data['postal_code']
        district = self.validated_data['district']
        image = self.validated_data.get('image')

        # Validate passwords
        if password != confirm_password:
            raise serializers.ValidationError({'error': "Passwords do not match."})

        # Check if email is unique
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email already exists."})
        
        if Seller.objects.filter(mobile_no=mobile_no).exists():
            raise serializers.ValidationError({'error': "Mobile number already exists."})

        account = User(username=username, first_name=first_name, last_name=last_name, email=email)
        account.set_password(password)
        account.is_active = False  
        account.save()
        print("ACCOUNT",account)

        seller = Seller(
            user=account,
            company_name=company_name,
            mobile_no=mobile_no,
            street_name=street_name,
            postal_code=postal_code,
            district=district,
            image = image,
        )
        seller.save()
        print("SELLER", seller)

        return account

    
class SellerLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)


class ReviewSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['created_on']

class ReviewGetSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False) 
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['created_on']

   