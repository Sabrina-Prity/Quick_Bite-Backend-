
from django.urls import path
from . import views

urlpatterns = [
    path('create-cart/', views.CartCreateApiView.as_view(), name='create-cart'),
    path('cart-details/<int:pk>/', views.CartDetailsView.as_view(), name='cart-details'),
    path('cart-item/', views.AddFoodIntoCartWithCartId.as_view(), name='add-food-to-cart'),
    path('see-cart-item/<int:cart_id>/', views.SeeCartItemAPIView.as_view(), name='see-cart-items'),
    path('see-cart-items-for-seller/<int:cart_id>/<int:seller_id>/', views.SeeCartItemforSellerAPIView.as_view(), name='see-cart-items-for-seller'),
    path('cart-item/update/<int:pk>/', views.CartItemsUpdate.as_view(), name='update-cart-item'),
    path('clear-seller-cart/<int:cart_id>/<int:seller_id>/', views.ClearCartItemsView.as_view(), name='clear_seller_cart'),
]
