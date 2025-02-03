from django.db import models
from customer.models import Customer
from food.models import FoodItem
from cart.models import CartItem
from seller.models import Seller

# Create your models here.

class Order(models.Model):
    BUYING_STATUS = [
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
        ('Pending', 'Pending'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    buying_status = models.CharField(choices=BUYING_STATUS, max_length=10, default="Pending")
    mobile = models.CharField(max_length=12, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    full_address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} for {self.customer.user.first_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name} in Order {self.order.id}"
    
    # def get_total(self):
    #     total = self.food_item.price * self.quantity
    #     float_total = format(total, '0.2f')
    #     return float_total

    
    

