
from django.urls import path, include
from . import views



urlpatterns = [
    path('list/', views.CategoryAPIView.as_view()),
    path('list/<int:pk>/', views.CategoryAPIView.as_view(), name='category-detail'),
    path('seller_category_list/<int:seller_id>/', views.SellerCategoryAPIView.as_view(), name='seller_category_list'),
    path('delete_seller_category/<int:seller_id>/<int:pk>/', views.SellerCategoryAPIView.as_view(), name='delete_seller_category'),
]