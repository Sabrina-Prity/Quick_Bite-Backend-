
from django.urls import path, include
from . import views


urlpatterns = [
    path('register/', views.CustomerRegistrationView.as_view(), name='register'),
    path('login/', views.CustomerLoginApiView.as_view(), name='login'),
    path('logout/', views.CustomerLogoutView.as_view(), name='logout'),
    path('customer-list/', views.CustomerListView.as_view(), name='customer-list'),
    path('customer-detail/<int:user_id>/', views.CustomerDetailView.as_view(), name='customer-detail'),
]
