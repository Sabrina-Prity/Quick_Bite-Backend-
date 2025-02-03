from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderGetSerializer,OrderSeeSerializer
from customer.models import Customer
from cart.models import CartItem, Cart
from seller.models import Seller
from rest_framework.permissions import AllowAny
from cart.serializers import CartItemForOrderSerializer
from food.models import FoodItem
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from payment.models import Payment_Model



class PlaceOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, cart_id, seller_id, format=None):
        # Get cart items from request body
        cart_items_data = request.data.get('cart_items', [])

        # Check if cart_items is empty
        if not cart_items_data:
            return Response({"message": "Cart items are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Process the rest of the data
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        # Filtering cart items for the given seller
        cart_items = CartItem.objects.filter(cart=cart, food_item__seller__id=seller_id)

        if not cart_items.exists():
            return Response({"message": "No items found for this seller in the cart"}, status=status.HTTP_404_NOT_FOUND)

        # Extract customer information from request
        user = request.user
        customer = user.customer
        mobile = request.data.get('mobile')
        district = request.data.get('district')
        full_address = request.data.get('full_address')

        if not all([mobile, district, full_address]):
            return Response({"message": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the order
        order = Order.objects.create(
            customer=customer,
            seller=cart_items.first().food_item.seller,
            mobile=mobile,
            district=district,
            full_address=full_address,
            buying_status='pending',  # Default status
        )

        # Create order items from cart items
        for item in cart_items_data:
            try:
                food_item = FoodItem.objects.get(id=item['food_item'])
            except FoodItem.DoesNotExist:
                return Response({"message": f"Food item with ID {item['food_item']} not found"}, status=status.HTTP_400_BAD_REQUEST)

            # Create the order item
            cart_item = cart_items.filter(food_item=food_item).first()
            if cart_item:
                OrderItem.objects.create(
                    order=order,
                    food_item=food_item,
                    quantity=item['quantity'],   # Use the quantity from the request data
                    price=item['price']          # Use the price from the request data
                )

        # Delete cart items for this seller
        cart_items.delete()

        # Serialize the order
        serialized_order = OrderSerializer(order)

        return Response({
            "message": "Order placed successfully",
            "order": serialized_order.data,
        }, status=status.HTTP_201_CREATED)



class OrdersBySellerView(APIView):
    def get(self, request, seller_id, format=None):
        # Get all order items related to the seller
        order_items = OrderItem.objects.filter(food_item__seller__id=seller_id)
        
        if not order_items.exists():
            return Response({"message": "No orders found for this seller"}, status=status.HTTP_404_NOT_FOUND)

        # Get all the orders associated with these order items
        orders = Order.objects.filter(order_items__in=order_items).distinct()

        # Serialize the orders using OrderSeeSerializer
        serialized_orders = OrderSeeSerializer(orders, many=True).data

        # Attach payment status to each order
        for order in serialized_orders:
            payment = Payment_Model.objects.filter(order_id=order["id"]).order_by('-payment_time').first()
            order["payment_status"] = payment.payment_status if payment else "Pending"

        return Response({
            "orders": serialized_orders
        }, status=status.HTTP_200_OK)





# class OrdersBySellerView(APIView):
#     def get(self, request, seller_id, format=None):
#         # Get all order items related to the seller
#         order_items = OrderItem.objects.filter(food_item__seller__id=seller_id)
        
#         if not order_items.exists():
#             return Response({"message": "No orders found for this seller"}, status=status.HTTP_404_NOT_FOUND)

#         # Get all the orders associated with these order items
#         orders = Order.objects.filter(order_items__in=order_items).distinct()

#         # Serialize the orders
#         serialized_orders = OrderSeeSerializer(orders, many=True)

#         return Response({
#             "orders": serialized_orders.data
#         }, status=status.HTTP_200_OK)




class AdminOrderUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self, request, *args, **kwargs):
        order = self.get_order(kwargs['pk'])
        if not order:
            return Response({"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get the new buying status from the request
        new_status = request.data.get('buying_status')

        # Update the order status if provided in the request
        if new_status:
            order.buying_status = new_status

        serializer = OrderGetSerializer(order, data=request.data, partial=True)
        
        if serializer.is_valid():
            # Save the order after validation
            serializer.save()

            # Now that the status is saved, check if the status was updated
            if new_status == 'Completed':
                self.send_order_completed_email(order)
                return Response({"message": "Order updated to 'Completed' and email sent."})

            elif new_status == 'Canceled':
                self.send_order_canceled_email(order)
                return Response({"message": "Order updated to 'Canceled' and email sent."})

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_order(self, order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    def send_order_completed_email(self, order):
        email_subject = "Your Order has been Completed"
        email_body = render_to_string(
            'order_completed_email.html',
            {
                'user': order.customer.user,
                'order_id': order.id,
                'items': order.order_items.all()
            }
        )
        print("Email sent")
        self.send_email(order.customer.user.email, email_subject, email_body)

    def send_order_canceled_email(self, order):
        email_subject = "Your Order has been Canceled"
        email_body = render_to_string(
            'order_canceled_email.html',
            {
                'user': order.customer.user,
                'order_id': order.id,
                'items': order.order_items.all(),
                'reason': "Unfortunately, we couldn't process your order at this time."
            }
        )
        self.send_email(order.customer.user.email, email_subject, email_body)

    def send_email(self, to_email, subject, body):
        email = EmailMultiAlternatives(subject, '', to=[to_email])
        email.attach_alternative(body, "text/html")
        email.send()


class UserOrdersView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, user_id, format=None):
        user = User.objects.get(id=user_id)
        customer = request.user.customer

        # Retrieve all orders associated with this customer
        orders = Order.objects.filter(customer=customer).order_by('-created_at')

        order_list = []
        for order in orders:
            # Fetch the latest payment status for this order
            payment = Payment_Model.objects.filter(order=order).order_by('-payment_time').first()
            payment_status = payment.payment_status if payment else "Pending"  # Default to "Pending"

            order_data = {
                "id": order.id,
                "buying_status": order.buying_status,
                "created_at": order.created_at,
                "payment_status": payment_status,  # Add payment status to response
                "order_items": [
                    {
                        "food_item": {
                            "name": item.food_item.name,
                            "price": str(item.food_item.price),
                        },
                        "quantity": item.quantity,
                    }
                    for item in order.order_items.all()
                ],
            }
            order_list.append(order_data)

        return Response(order_list, status=status.HTTP_200_OK)

# class UserOrdersView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [TokenAuthentication]

#     def get(self, request,user_id, format=None):

#         user = User.objects.get(id=user_id)
#         customer = request.user.customer

#         # Retrieve all orders associated with this customer
#         orders = Order.objects.filter(customer=customer).order_by('-created_at')  # Sort by latest orders

#         # Serialize the orders
#         serializer = OrderSeeSerializer(orders, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)
    

class DeleteOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]  
    authentication_classes = [TokenAuthentication]
    
    def delete(self, request, order_id, format=None):
        user_id = request.user.id  # Get the ID of the authenticated user
        
        try:
            # Fetch the order using the provided order_id and ensure it belongs to the authenticated user
            order = Order.objects.get(pk=order_id, customer__id=user_id)

            # Check the status of the order before deletion
            if order.buying_status not in ["Completed", "Canceled"]:
                return Response({
                    "error": "Order can only be deleted if its status is 'Completed' or 'Canceled'."
                }, status=400)

            # If the order is valid for deletion, delete the order and related order items
            order_items = order.order_items.all()
            print(f"Deleting OrderItems: {order_items}")

            # Delete the order (Django will cascade delete related OrderItems automatically)
            order.delete()

            # Respond with a success message and the updated list of orders
            updated_orders = Order.objects.filter(customer__id=user_id)
            serializer = OrderGetSerializer(updated_orders, many=True)
            return Response({
                "message": "Order deleted successfully.",
                "updated_orders": serializer.data
            })
        
        except Order.DoesNotExist:
            return Response({"error": "Order not found for this user."}, status=404)