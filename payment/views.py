from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from .models import Payment_Model
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from sslcommerz_lib import SSLCOMMERZ
import uuid
from django.http import HttpResponseRedirect
from rest_framework.authentication import TokenAuthentication
from order.models import Order
from cart.models import Cart
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class Payment_View(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        print("29 line",request.user)
        order_id = request.data.get('order_id')
        total_price = request.data.get('total_amount')
        total_item = request.data.get('total_item')
        user_id = request.data.get('user_id')
        print("user_id", user_id)

        try:
            order = Order.objects.get(id=order_id)
            mobile = order.mobile
        except Order.DoesNotExist:
            return Response({"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        settings_data = {
            "store_id": 'quick67964e00ba379',
            "store_pass": 'quick67964e00ba379@ssl',
            "issandbox": True,
        }

        
        sslcz = SSLCOMMERZ(settings_data)

        transaction_id = f"TXN-O{order_id}U{request.user.id}-{str(uuid.uuid4())[:8].upper()}"
        post_body = {
            "total_amount": total_price,
            "currency": "BDT",
            "tran_id": transaction_id,
            "success_url": f"http://127.0.0.1:8000/successs/?user_id={request.user.id}",
            # "success_url": f"http://127.0.0.1:8000/successs/",
            "fail_url": f"{settings.BASE_URL}/fail/",        
            "cancel_url": f"{settings.BASE_URL}/cancel/",    
            "emi_option": 0,
            "cus_name": request.user.username,
            "cus_email": request.user.email,
            "cus_phone": mobile,
            "cus_add1": "address",
            "cus_city": "Dhaka",
            "cus_country": "Bangladesh",
            "shipping_method": "NO",
            "product_name": f"Order {order.id}",
            "num_of_item": total_item,
            "product_category": "Order",
            "product_profile": "general",
        }

        response = sslcz.createSession(post_body)

        if response.get("status") == "SUCCESS":
            try:
                # Store user ID in session before redirecting
                request.session['user_id'] = request.user.id 

                Payment_Model.objects.create(
                    user=request.user,
                    order=order,
                    amount=total_price,
                    payment_status="Pending",
                    transaction_id=transaction_id,
                )

                return Response(
                    {
                        "status": "success",
                        "tran_id": transaction_id,
                        "message": f"Payment successfully initiated for order ID {order.id}",
                        "payment_url": response.get("GatewayPageURL"),
                    },
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {
                        "status": "error",
                        "message": "Failed to create payment entry.",
                        "details": str(e),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            order.buying_status = "Canceled"
            order.save()

            return Response(
                {
                    "status": "error",
                    "message": "Payment session creation failed.",
                    "details": response,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF for external requests
class PaymentSuccess_View(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):  # Handle POST requests
        return self.process_payment(request)

    def get(self, request):  # Handle GET requests
        return self.process_payment(request)

    def process_payment(self, request):
        transaction_id = request.GET.get("tran_id") or request.data.get("tran_id")

        if not transaction_id:
            return Response({"message": "Transaction ID missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment_Model.objects.get(transaction_id=transaction_id)
            payment.payment_status = "Completed"
            payment.save()

            
            # order = payment.order  
            # order.buying_status = "Completed"
            # order.save()

            return redirect(f"http://127.0.0.1:5500/customer_orders.html")

            # return Response(
            #     {"message": "Payment successful!", "transaction_id": transaction_id},
            #     status=status.HTTP_200_OK
            # )
        except Payment_Model.DoesNotExist:
            return Response(
                {"message": "Invalid transaction"}, status=status.HTTP_400_BAD_REQUEST
            )




@method_decorator(csrf_exempt, name='dispatch')
class PaymentFail_View(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        tran_id = request.data.get('tran_id')

        try:
            payment = Payment_Model.objects.get(transaction_id=tran_id)
            payment.payment_status = 'Canceled'
            payment.save()

            # order = payment.order
            # order.buying_status = 'Canceled'
            # order.save()

            return HttpResponseRedirect(f"http://127.0.0.1:5500/index.html")  # Updated URL
        except Payment_Model.DoesNotExist:
            return Response({'message': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)



@method_decorator(csrf_exempt, name='dispatch')
class PaymentCancel_View(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        tran_id = request.data.get('tran_id')

        try:
            payment = Payment_Model.objects.get(transaction_id=tran_id)
            payment.payment_status = 'Canceled'
            payment.save()

            # order = payment.order
            # order.buying_status = 'Canceled'
            # order.save()

            return HttpResponseRedirect(f"http://127.0.0.1:5500/index.html")  # Updated URL
        except Payment_Model.DoesNotExist:
            return Response({'message': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

