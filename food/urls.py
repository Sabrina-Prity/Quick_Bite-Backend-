from django.urls import path
from . import views

urlpatterns = [
    path('food-items/', views.FoodItemListForAuthenticatedSellerView.as_view(), name='food-items-for-seller'),
    path('food-item/<int:seller_id>/', views.FoodItemCreateView.as_view(), name='food-item-list-create'),
    path('food-item/get/<int:pk>/', views.FoodItemDeleteView.as_view(), name='get-food-item'),
    path('food-item/delete/<int:pk>/<int:seller_id>/', views.FoodItemDeleteView.as_view(), name='delete-food-item'),
    path('food-items-for-seller/<int:seller_id>/', views.FoodItemListpecificSellerView.as_view(), name='food-items-for-seller'),
    path('comment/', views.AllCommentView.as_view(), name='comment'),
    path('comment/<int:food_id>/<int:seller_id>/', views.CommentListView.as_view(), name='comment-list-create'),
    path('comments/<int:comment_id>/delete/', views.CommentUpdateView.as_view(), name='comment-delete'),

   
]