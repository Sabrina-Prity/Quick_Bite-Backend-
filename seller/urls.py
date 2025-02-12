
from django.urls import path, include
from . import views


urlpatterns = [
    path('districts/', views.DistrictChoicesView.as_view(), name='district-choices'),
    path('register/', views.SellerRegistrationView.as_view(), name='register'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
    path('login/', views.SellerLoginApiView.as_view(), name='login'),
    path('logout/', views.SellerLogoutView.as_view(), name='logout'),
    path('seller-list/', views.SellerListView.as_view(), name='seller-list'),
    path('seller-detail/<int:pk>/', views.SellerDetailView.as_view(), name='seller-detail'),
    path('seller-details-update/<int:seller_id>/', views.SellerDetailsUpdateView.as_view(), name='seller-details-update'),
    path('reviews/<int:seller_id>/', views.SellerReviewListCreateDeleteView.as_view(), name='seller-review-list-create'),
    path('reviews/delete/<int:seller_id>/<int:pk>/', views.SellerReviewListCreateDeleteView.as_view(), name='seller-review-delete'),
    path('seller/<int:seller_id>/average-rating/', views.SellerAverageRatingView.as_view(), name='seller-average-rating'),
    path('sellers/average-rating/', views.AllSellersAverageRatingView.as_view(), name='all-sellers-average-rating'),
]


