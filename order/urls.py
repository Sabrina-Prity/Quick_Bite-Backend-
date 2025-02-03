from django.urls import path
from . import views



urlpatterns = [
    path('place-order/<int:cart_id>/<int:seller_id>/', views.PlaceOrderView.as_view(), name="place_order"),
    path('seller-orders/<int:seller_id>/', views.OrdersBySellerView.as_view(), name='seller-orders'),
    path('admin-order-updated/<int:pk>/', views.AdminOrderUpdateAPIView.as_view(), name='admin-order-updated'),
    path('orders-view/<int:user_id>/', views.UserOrdersView.as_view(), name='user-orders'),
    path('orders-delete/<int:order_id>/', views.DeleteOrderView.as_view(), name='orders-delete'),
]