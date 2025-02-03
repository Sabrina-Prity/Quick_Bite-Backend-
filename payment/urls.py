from django.urls import path
from .views import Payment_View, PaymentSuccess_View, PaymentFail_View, PaymentCancel_View

urlpatterns = [
    path('pay/', Payment_View.as_view(), name='post_payment'),
    path('successs/',PaymentSuccess_View.as_view(), name='payment_success'),
    path('fail/', PaymentFail_View.as_view(), name='payment_fail'),
    path('cancel/', PaymentCancel_View.as_view(), name='payment_cancel'),
]
